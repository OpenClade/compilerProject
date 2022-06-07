# import serializers
from enum import unique
from pkg_resources import require
from rest_framework import serializers
from main.models import *
from user.models import *
from django import forms


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProgrammingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingTask
        fields = "__all__"
        extra_kwargs = {'created_by': {'read_only': True}}


class ProgrammingTaskSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingTaskSolution
        fields = ("id", "task", "author", "language", "code", "is_public", "created_at")
        extra_kwargs = {'author': {'read_only': True}}


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    surname = forms.CharField(max_length=32)
    group = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=32)
    unique_number = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('first_name', 'surname', 'group', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class ProgrammingTaskSolutionForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea, max_length=10000, required=False)
    code.widget.attrs['display'] = 'none'
    file = forms.FileField(required=False)
    file.widget.attrs['class'] = 'custom-file-input'

    class Meta:
        model = ProgrammingTaskSolution
        fields = ("code", "file")
        extra_kwargs = {'author': {'read_only': True}}


class UserFormLogin(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=32)


# title description slug time_limit memory_limit author language 

class CourseForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.TextInput()
    slug = forms.SlugField(max_length=100)
    banner = forms.ImageField()

    class Meta:
        model = Course
        fields = ('title', 'description', 'slug', 'banner')
        extra_kwargs = {'author': {'read_only': True}}
