from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# from forms import EmailUserCreationForm, EmailUserChangeForm
# from models import EmailUser


# class EmailUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                       'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2')}),
#     )

#     form = EmailUserChangeForm
#     add_form = EmailUserCreationForm
#     list_display = ('email', 'is_staff',)
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
#     search_fields = ('email',)
#     ordering = ('email',)


# # Don't register admin unless user model is EmailUserAdmin
# user_model = get_user_model()
# if user_model == EmailUser:
#     admin.site.register(user_model, EmailUserAdmin)
