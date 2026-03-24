from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 "
    "focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Seu usuário'})
        self.fields['password'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Sua senha'})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': INPUT_CLASS})
