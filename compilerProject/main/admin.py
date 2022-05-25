from django.contrib import admin
from main.models import ProgrammingTask, ProgrammingTaskSolution, User, Course, Chapter, Tests

admin.site.register(ProgrammingTask)
admin.site.register(ProgrammingTaskSolution)
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Tests)
