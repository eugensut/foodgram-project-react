from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow

DEFAULT_EMPTY_VALUE = '-empty-'


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff')
    list_filter = ('email', 'username')
    empty_value_display = DEFAULT_EMPTY_VALUE


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow)
