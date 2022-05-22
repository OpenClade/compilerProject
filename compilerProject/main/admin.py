from django.contrib import admin
from main.models import ProgrammingTask, ProgrammingTaskSolution, User

admin.site.register(ProgrammingTask)
admin.site.register(ProgrammingTaskSolution)
admin.site.register(User)

