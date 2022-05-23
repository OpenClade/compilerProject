from django.contrib import admin
from django.contrib.auth.models import User
from user.models import Student, Teacher


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active')
    list_filter = ('is_active', 'is_staff', 'role')
    search_fields = ('username', 'email')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')
    list_editable = ('is_active',)
    list_per_page = 10
    list_select_related = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),


        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

 
admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)