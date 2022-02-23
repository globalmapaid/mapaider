from django.contrib.auth.forms import UserCreationForm as StdUserCreationForm, UserChangeForm as StdUserChangeForm

from .models import User


class UserCreationForm(StdUserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(StdUserChangeForm):

    class Meta:
        model = User
        fields = ('email',)