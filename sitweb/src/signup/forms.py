import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Exemple: +33769604783'}),
        }
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Use a regular expression to check the phone number format
        if not re.match(r'^\+\d{11}$', phone_number):
            raise forms.ValidationError('Please enter a valid phone number in the format +33769604783.')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Your custom validation logic for email
        # For example, check if the email is unique
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class CustomAuthenticationForm(AuthenticationForm):
    pass
