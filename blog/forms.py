from django.forms import ModelForm
from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group, auth

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'descriptions','thumbnail', 'body', 'category',)

class CommentForm(ModelForm):
    # text = forms.CharField(widget = CKEditorWidget(config_name='normal_user'), label='Add your comment')
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': _('')
        }
        widgets = {
            'text': forms.Textarea(
				attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'write your comment here',
                    'rows': '3',
                }),
			}

class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2',
                    'required': True
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control text-capitalize mb-2',
                    'required': True
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control text-capitalize mb-2',
                    'required': True
                }
            )
        }