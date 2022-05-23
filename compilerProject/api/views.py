from pprint import pprint

from django.shortcuts import render
from rest_framework import generics
from api.serializers import *
from main.models import *
from user.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import sys
from io import StringIO
from rest_framework.status import *
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserView(generics.CreateAPIView):
#     renderer_classes = [TemplateHTMLRenderer] 
#     permission_classes = [AllowAny,]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer  
#     template_name = 'onlineCoding/authorization.html'


#     def get(self, request, *args, **kwargs):
#         return Response(status=HTTP_200_OK)

#     def post(self, request):
#         user = User.objects.create_user(**request.data)
#         user.set_password(request.data['password'])
#         user.save()
#         serializer = UserSerializer(user, data=request.data)
#         if not serializer.is_valid():
#             return Response({'serializer': serializer, 'user': user})
#         serializer.save()
#         return redirect('profile-list')


class ProgrammingTaskDetail(generics.RetrieveAPIView):
    queryset = ProgrammingTask.objects.all()
    serializer_class = ProgrammingTaskSerializer


class ProgrammingTaskSolutionDetail(generics.RetrieveAPIView):
    queryset = ProgrammingTaskSolution.objects.all()
    serializer_class = ProgrammingTaskSolutionSerializer


class ProgrammingTaskSolutionView(generics.CreateAPIView):
    queryset = ProgrammingTaskSolution.objects.all()
    serializer_class = ProgrammingTaskSolutionSerializer

    def create(self, request, *args, **kwargs):
        try:
            old_stdout = sys.stdout
            x = StringIO()
            mystdout = sys.stdout = x
            exec(request.data['code'])
            sys.stdout = old_stdout
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        serializer = ProgrammingTaskSolutionSerializer(data=request.data)
        mystdout.getvalue().replace("\n", "")
        if serializer.is_valid():

            task = ProgrammingTask.objects.get(id=request.data['task'])
            print(task.output_example + " " + mystdout.getvalue())

            if task.output_example.strip() == mystdout.getvalue().strip():
                print(1)
                return Response({"answer": "you are right!", "programming_solution": serializer.data,
                                 "execute": mystdout.getvalue().replace('\n', "")}, status=HTTP_200_OK)
            else:
                return Response({"answer": "you are not right!", "programming_solution": serializer.data,
                                 "execute": mystdout.getvalue().replace('\n', "")}, status=HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class ProgrammingTaskView(generics.ListCreateAPIView):
    queryset = ProgrammingTask.objects.all()
    serializer_class = ProgrammingTaskSerializer


# view for textEditor.html
class TextEditorView(generics.ListCreateAPIView):
    queryset = ProgrammingTaskSolution.objects.all()
    serializer_class = ProgrammingTaskSolutionSerializer
    template_name = 'onlineCoding/textEditor.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def create(self, request, *args, **kwargs):
        serializer = ProgrammingTaskSolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'onlineCoding/welcome.html')


def auth(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('problems')
        form = UserForm()
        loginform = UserFormLogin()
        return render(request, 'onlineCoding/authorization.html', {'form': form, 'loginform': loginform})

    elif request.method == 'POST':

        loginform = UserFormLogin(request.POST)

        if loginform.is_valid():
            pprint(request.POST['email'])
            pprint(request.POST['password'])
            username = loginform.cleaned_data['email']
            password = loginform.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('problems')
            else:
                return redirect('auth')
        form = UserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            request.user = user
            return render(request, 'onlineCoding/profile.html')

        else:
            return render(request, 'onlineCoding/authorization.html')


def base(request):
    return render(request, 'onlineCoding/base.html')


def problems(request):
    tasks = ProgrammingTask.objects.all()
    return render(request, 'onlineCoding/problems.html', {'tasks': tasks})


def textEditor(request, slug):
    if request.method == 'GET':
        task = get_object_or_404(ProgrammingTask, slug=slug)
        form = ProgrammingTaskSolutionForm()
        # if request.user.is_authenticated:
        return render(request, 'onlineCoding/textEditor.html', {'task': task})
        # else:
        #     return render(request, 'onlineCoding/problempage.html')
    elif request.method == 'POST':
        # create object ProgrammingTaskSolution
        task = get_object_or_404(ProgrammingTask, slug=slug)
        print(request.POST)
        form = ProgrammingTaskSolutionForm(code=request.POST['code'], user=request.user)
        if form.is_valid():
            new_solution = form.save(commit=False)
            new_solution.user = request.user
            new_solution.task = task
            new_solution.save()
            return redirect('textEditor', slug=slug)
        return render(request, 'onlineCoding/textEditor.html', {'task': task})


def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'onlineCoding/profile.html')
        else:
            return render(request, 'onlineCoding/problempage.html')


def leaderboard(request):
    users = User.objects.all().order_by('rating').reverse()
    return render(request, 'onlineCoding/leaderboard.html', {'users': users})


def courses(request):
    courses = Course.objects.all()
    return render(request, 'onlineCoding/courses.html', {'courses': courses})


def coursePage(request, slug):
    try:
        course = get_object_or_404(Course, slug=slug)
        return render(request, 'onlineCoding/coursePage.html', {'course': course})
    except:
        return not_found_view(request)


def logout_view(request):
    logout(request)
    return redirect('auth')

def not_found_view(request):
    return render(request, 'onlineCoding/404.html')