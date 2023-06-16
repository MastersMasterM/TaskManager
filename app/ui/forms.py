"""
Custom Forms
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255)

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
        self.fields['password'].widget.attrs.update({'autofocus': False})
    
    class Meta:
        fields = ('email', 'password')

