from django import forms
from .models import Image
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image  # Replace 'Image' with your actual model name
        fields = ['image']  # Specify the field name for the image

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Remove help text for username
        self.fields['username'].help_text = ''
        # Remove help text for password1
        self.fields['password1'].help_text = ''
        # Remove help text for password2
        self.fields['password2'].help_text = ''

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if any(char.isdigit() for char in username):
            raise ValidationError('Username cannot contain numbers.')
        return username


    
