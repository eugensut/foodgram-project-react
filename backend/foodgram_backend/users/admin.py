from django.contrib import admin

from .models import User, Follow

DEFAULT_EMPTY_VALUE = '-empty-'


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')
    empty_value_display = DEFAULT_EMPTY_VALUE


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
