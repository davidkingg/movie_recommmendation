from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import MyUser


class UserEdit(UserChangeForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = MyUser
        fields = ("email", "first_name", "last_name", "image")

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user
