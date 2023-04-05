from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('comment_text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'main_text', 'category', 'image')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('avatar', 'bio', 'address')
