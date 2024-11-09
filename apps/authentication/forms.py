from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=20,
        min_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': 'autofocus', })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    password = forms.CharField(
        min_length=8,
        required=True,
        validators=[validate_password],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',

        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Username already exists')
        return email


