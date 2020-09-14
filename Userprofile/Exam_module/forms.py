from django import forms
from Exam_module import models
from django.contrib.auth.forms import UserCreationForm


class SubjectForm(forms.ModelForm):
    class Meta:
        model = models.Subject
        fields = ['name', 'code', 'sem', 'dept', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Subject Name', 'class': 'form-control'}),
            'code': forms.TextInput(attrs={'placeholder': 'Subject Code', 'class': 'form-control'}),
            'sem': forms.Select(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = models.Exam
        fields = ['name', 'start_date','end_date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Exam Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'date', 'class': 'vDateField'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'date', 'class': 'vDateField'}),
        }


class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = models.QuestionPaper
        fields = ['subject', 'duration', 'max_marks', 'datetime']
        widgets = {
            'subject': forms.Select(attrs={'placeholder': 'Subject Name', 'class': 'form-control'}),
            'datetime': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'duration': forms.TimeInput(attrs={'placeholder': 'Duration', 'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['question', 'max_marks', 'a', 'b', 'c', 'd', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'cols': 100, 'rows': 4, 'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'cols': 100, 'rows': 4, 'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs={'placeholder': 'Max Marks', 'class': 'form-control'}),
            'a': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Option A', 'class': 'form-control'}),
            'b': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Option B', 'class': 'form-control'}),
            'c': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Option C', 'class': 'form-control'}),
            'd': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Option D', 'class': 'form-control'}),
        }
