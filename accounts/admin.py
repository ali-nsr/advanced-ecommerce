from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserCreateForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = (
        'email', 'phone', 'first_name', 'last_name', 'is_superuser', 'is_admin', 'is_verify', 'has_setting_access',
        'is_editor', 'is_writer',
        'is_active', 'jalali_created_date')
    list_filter = ('email', 'is_active')
    fieldsets = (
        ('کاربر', {'fields': ('email', 'password')}),
        ('اطلاعات حساب کاربری', {'fields': ('first_name', 'last_name', 'phone', 'province', 'city',
                                            'post_code', 'address', 'image', 'temp_code')}),
        ('دسترسی ها',
         {'fields': (
             'is_superuser', 'is_active', 'is_verify', 'has_setting_access', 'is_admin', 'is_writer', 'is_editor')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'phone', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
