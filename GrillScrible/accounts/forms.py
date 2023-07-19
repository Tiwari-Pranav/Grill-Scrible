from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ("username","email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ("username","email")
