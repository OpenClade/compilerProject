from pprint import pprint

from django.shortcuts import render
from rest_framework import generics
from api.serializers import *
from main.models import *

from user.models import User, Teacher, Student
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import sys
from io import StringIO
from rest_framework.status import *
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from core.utils import plagiarism


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        if request.POST.get('group'):

            form = UserForm(request.POST)
            exists = User.objects.filter(email=request.POST['email']).exists()
            if form.is_valid() and not exists:
                unique_number = form.cleaned_data.pop('unique_number')
                user = User.objects.create_user(**form.cleaned_data)
                user.set_password(form.cleaned_data['password'])
                user.save()
                teacher = Teacher.objects.all().filter(uniquenumber=unique_number).first()
                if teacher:
                    Student.objects.create(user=user, teacher=teacher)
                else:
                    Student.objects.create(user=user, teacher=None)
                    # set current user
                user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
                login(request, user)
                return redirect('problems')
            else:
                return redirect('auth')
        else:

            loginform = UserFormLogin(request.POST)

            if loginform.is_valid():

                username = loginform.cleaned_data['email']
                password = loginform.cleaned_data['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('problems')
                else:
                    return redirect('auth')


def base(request):
    return render(request, 'onlineCoding/base.html')


def problems(request):
    print(request.user)
    tasks = ProgrammingTask.objects.all()
    for i in tasks:
        i.description = i.description[0:40] + "..."
    return render(request, 'onlineCoding/problems.html', {'tasks': tasks})


def textEditor(request, slug):
    if request.method == 'GET':
        task = get_object_or_404(ProgrammingTask, slug=slug)
        form = ProgrammingTaskSolutionForm()
        # if request.user.is_authenticated:
        first_test = Tests.objects.all().filter(task=task).first()
        tasksolution = ProgrammingTaskSolution.objects.filter(task=task, author=request.user).first()
        if tasksolution:
            return render(request, 'onlineCoding/textEditor.html',
                {
                    'first_test': first_test,
                    'task': task,
                    'form': form,
                    'type': 'warning',
                    'error': "You have already solved this task"
                }
            )
        return render(request, 'onlineCoding/textEditor.html', {'task': task, 'form': form, 'first_test': first_test})
        # else:
        #     return render(request, 'onlineCoding/problempage.html')
    elif request.method == 'POST' and request.user.is_authenticated and request.POST['code']:
        # create object ProgrammingTaskSolution
        task = get_object_or_404(ProgrammingTask, slug=slug)
        form = ProgrammingTaskSolutionForm()
        tasksolution = ProgrammingTaskSolution.objects.filter(task=task, author=request.user).first()
        first_test = Tests.objects.all().filter(task=task).first()
        if tasksolution:
            return render(request, 'onlineCoding/textEditor.html',
                {
                    'first_test': first_test,
                    'task': task,
                    'form': form,
                    'type': 'warning',
                    'error': "You have already solved this task"
                }
            )
        try:
            old_stdout = sys.stdout
            x = StringIO()
            mystdout = sys.stdout = x
            exec(request.POST['code'])
            sys.stdout = old_stdout
        except Exception as e:
            return render(request, 'onlineCoding/textEditor.html', {'task': task, 'type': 'danger', 'error': str(e)})

        mystdout = mystdout.getvalue().replace("\n", "")
        tests = Tests.objects.all().filter(task=task)
        for test in tests:
            if test.output_data.strip() != mystdout.strip():
                return render(request, 'onlineCoding/textEditor.html',
                              {'task': task, 'type': 'danger', 'error': "Wrong answer!"})
        solutions = ProgrammingTaskSolution.objects.all()

        obj = ProgrammingTaskSolution.objects.create(code=request.POST['code'], task=task, author=request.user)
        if task.max_plagiarism > 0:
            for s in solutions:

                percent = plagiarism(s.code, request.POST['code'])

                if percent > task.max_plagiarism and s != obj:
                    obj.isplagiarized = True
                    obj.plagiat = round(percent, 2)
                    obj.save()

                    return render(request, 'onlineCoding/textEditor.html',
                                  {'task': task, 'error': 'plagiarism detected'})
        student = Student.objects.all().filter(user=request.user).first()
        if student:
            student.rating += task.rating
            student.save()
        first_test = Tests.objects.all().filter(task=task).first()
        return render(request, 'onlineCoding/textEditor.html',
                      {'task': task,'first_test': first_test, 'form': form, 'type': 'success', 'answer': "Correct!"})
    # else:
    #     return render(request, 'onlineCoding/textEditor.html',
    #                   {'task': task, 'form': form, 'answer': "you are not right!"})


def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'onlineCoding/profile.html')
        else:
            return render(request, 'onlineCoding/404.html')


def leaderboard(request):
    users = Student.objects.all().order_by('-rating')
    place = 1
    if request.user.is_authenticated:
        currentUser = request.user
        for u in users:
            pprint(u.user.email)
            if u.user.email == currentUser.email:
                break
            place += 1
    return render(request, 'onlineCoding/leaderboard.html',
                  {
                      'users': users,
                      'place': place
                  })


def courses(request):
    courses = Course.objects.all()
    return render(request, 'onlineCoding/courses.html', {'courses': courses})


def coursePage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    chapters = Chapter.objects.all().filter(course=course)
    tasks = ProgrammingTask.objects.all().filter(course=course)
    return render(request, 'onlineCoding/coursePage.html', {'course': course, 'chapters': chapters, 'tasks': tasks})


def logout_view(request):
    logout(request)
    return redirect('auth')


def not_found_view(request):
    return render(request, 'onlineCoding/404.html')


def teacher(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and Teacher.objects.all().filter(user=request.user).exists():
            teacher = Teacher.objects.all().filter(user=request.user).first()
            users_of_teachers = Student.objects.all().filter(teacher=teacher)
            plagiarism_tasks_solution = ProgrammingTaskSolution.objects.all().filter(task__teacher=teacher,
                                                                                     isplagiarized=True)
            return render(request, 'onlineCoding/teachers.html',
                          {'teacher': teacher, 'plagiarism_tasks': plagiarism_tasks_solution,
                           'users_of_teachers': users_of_teachers})

    return redirect('auth')


def solved(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            solved_tasks = ProgrammingTaskSolution.objects.all().filter(author=request.user)
            return render(request, 'onlineCoding/solved.html', {'solved_tasks': solved_tasks})
    return redirect('auth')
