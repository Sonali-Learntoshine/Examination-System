from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import ProfileDetail
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileDetailForm(ModelForm):
    class Meta:
        model = ProfileDetail
        fields = '__all__'

        semester = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8')
        )
        widgets = {
            'dob': forms.DateInput(format=('%m/%d/%Y'),
                                   attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                          'type': 'date'}),
            'sem': forms.Select(choices=semester, attrs={'class': 'form-control'}),
        }
