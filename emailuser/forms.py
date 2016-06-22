from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()


class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', )


class EmailUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
