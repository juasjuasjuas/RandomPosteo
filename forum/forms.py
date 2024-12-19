from django import forms
from .models import *

class UserPostForm(forms.ModelForm):

    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-style-3',
        'placeholder': 'Title',
    }))

    description = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control form-control-style-3',
        'placeholder': 'Description in detail...',
        'rows': '8',
        'cols': '80',
    }))

    image = forms.ImageField(label="Image (Optional)", required=False)  # Add ImageField

    class Meta:
        model = UserPost
        fields = ['title', 'description', 'image']  # Include 'image' in fields

class AnswerForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control form-control-style-3',
        'placeholder': 'Write your answer...',
        'rows': '8',
        'cols': '50',
    }))
    image = forms.ImageField(label="Image", required=False)  # Add ImageField

    class Meta:
        model = Answer
        fields = ['content', 'image']