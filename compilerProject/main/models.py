from django.db import models
from user.models import *
from core.choices import *


class ProgrammingTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=True)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=10)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, default='easy', max_length=10)
    max_plagiarism = models.FloatField(default=0)
    solved_count = models.IntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Programming Task'
        verbose_name_plural = 'Programming Tasks'


class Tests(models.Model):
    task = models.ForeignKey(ProgrammingTask, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.task.title

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'


class ProgrammingTaskSolution(models.Model):
    task = models.ForeignKey(ProgrammingTask, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=0)
    code = models.TextField()
    isplagiarized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    plagiat = models.FloatField(default=0)

    def __str__(self):
        return self.task.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Programming Task Solution'
        verbose_name_plural = 'Programming Task Solutions'


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='img', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='chapters', null=True, blank=True)
    information = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
