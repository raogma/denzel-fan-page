from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import AdminFileWidget

from DenzelProject.blogPost.models import Post, Comment
from DenzelProject.utils import ApplyStyleMixin


class CreatePostForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_bootstrap()
        self.set_labels()

    class Meta:
        model = Post
        fields = ('image', 'header', 'description')
        widgets = {
            'header': forms.TextInput(
                attrs={
                    'placeholder': 'Header'
                }
            ),
            'image': AdminFileWidget(),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                }
            ),
        }


class DeletePostForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_bootstrap()
        self.set_labels()
        self.disable_fields()

    def save(self, commit=True):
        res = super().save(commit=commit)
        self.instance.delete()
        return res

    class Meta:
        model = Post
        exclude = ('owner', 'image')
        widgets = {
            'header': forms.TextInput(
                attrs={
                    'placeholder': 'Header'
                }
            ),
            'image': AdminFileWidget(),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                }
            ),
        }


class SearchDashForm(forms.Form, ApplyStyleMixin):
    searched = forms.CharField(
        max_length=30,
        required=False,
        label='',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_bootstrap()


class CommentForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_bootstrap()

    class Meta:
        model = Comment
        fields = ('content', )


class DelCommentForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_bootstrap()

    class Meta:
        model = Comment
        fields = ('content', )


class UpCommentForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_bootstrap()

    class Meta:
        model = Comment
        fields = ('content', )