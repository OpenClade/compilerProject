from collections import UserList
from api.views import *
from django.urls import path

from core import settings

urlpatterns = [
    # path('login/', UserView.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('programmingtasks/', ProgrammingTaskView.as_view()),
    path('programmingtasks/<int:pk>/', ProgrammingTaskDetail.as_view()),
    path('programmingtasksolutions/', ProgrammingTaskSolutionView.as_view()),
    path('programmingtasksolutions/<int:pk>/', ProgrammingTaskSolutionDetail.as_view()),
    path('texteditor/', TextEditorView.as_view()),

]

