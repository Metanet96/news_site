from django import forms

from front import models

from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = '__all__'



class PostForm(forms.ModelForm):

    class Meta:
        model = models.Post
        fields = '__all__'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password1', 'password2', )