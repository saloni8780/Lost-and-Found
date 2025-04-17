from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LostFoundItem
from django import forms

class CollegeUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@nie.ac.in'):
            raise forms.ValidationError("Use your NIE college email")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.upper()  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.upper()  
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':"Enter your USN" }),
            'email': forms.EmailInput(attrs={'class': 'form-control',}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control' }),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
     

    
class LostFoundItemForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = LostFoundItem
        fields = ['name', 'email', 'phone', 'title', 'description', 'item_type', 'location', 'date', 'image']
