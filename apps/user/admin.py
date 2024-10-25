from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjUserAdmin

from django.utils.translation import gettext_lazy as _

from apps.user.models import User

from .models import User


@admin.register(User)
class UserAdmin(DjUserAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Perms'), {'fields': ('is_admin', 'is_active',)}),
    )
    ordering = ('email',)
