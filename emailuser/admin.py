from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import EmailUserCreationForm, EmailUserChangeForm
from .models import EmailUser


class EmailUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )

    form = EmailUserChangeForm
    add_form = EmailUserCreationForm
    list_display = ('email', 'is_staff',)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(EmailUser, EmailUserAdmin)
