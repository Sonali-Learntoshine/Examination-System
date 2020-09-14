from django.contrib.auth.forms import UserCreationForm
from .models import Contact
from . import models
from django import forms


class StudentSignupForm(UserCreationForm):
    class Meta:
        model = models.Student
        fields = ['user_id', 'first_name', 'last_name', 'email', 'profile_image', 'sem', 'dept',
                  'date_of_birth', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}),
            'profile_image': forms.FileInput(),
            'sem': forms.Select(attrs={'placeholder': 'select', 'class': 'form-control'}),
            'dept': forms.Select(attrs={'placeholder': 'select', 'class': 'form-control'}),
            'user_id': forms.NumberInput(attrs={'placeholder': 'University Roll Number', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'vDateField'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
