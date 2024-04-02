from django import forms
from django.contrib.auth.models import User
from .models import Member
from myapp import models

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # Ensure valid email format

    class Meta:
        model = User
        fields = ['username', 'email']  # Adjust fields as needed

    def clean_email(self):
        email = self.cleaned_data['email']
        # Add email uniqueness check if desired (consider using django-registration or a similar library for advanced user management)

        return email

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        phonenumber = +254
        fields = ['name', 'phonenumber']  # Adjust fields as needed