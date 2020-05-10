from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Данные пользователя', {'fields': ('email', 'username', 'password', 'name', 'surname', 'phone')}),
        ('Разрешения', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            'Изменить пароль',
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2')
            }
        ),
    )
    list_display = ('email', 'username', 'name', 'surname', 'is_staff', 'phone', 'date_of_add')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'name', 'surname')
    ordering = ('last_login',)
    filter_horizontal = ('user_permissions',)


admin.site.register(User, UserAdmin)
