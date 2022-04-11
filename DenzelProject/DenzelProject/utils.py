from django import forms
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from DenzelProject.blogPost.models import Post, Comment


class ApplyStyleMixin:
    def disable_fields(self):
        for field in self.fields:
            self.fields[field].disabled = True

    def apply_style_w3(self):
        for field in self.fields:
            if field == 'gender':
                self.fields[field].widget.attrs['class'] = 'w3-select w3-border'
                continue
            self.fields[field].widget.attrs['class'] = 'w3-input'

    def apply_style_bootstrap(self):
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def set_labels(self):
        label_data = {
            # reg form
            'avatar': 'Profile Picture',
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'gender': 'Gender',
            'address': '',
            'email': '',
            'password1': '',
            'password2': '',
            # login form
            'username': '',
            'password': '',
            # post form
            'header': '',
            'description': '',
            'image': 'Image:'
        }
        for field_name in self.fields:
            self.fields[field_name].label = label_data[field_name]

    def remove_help_text(self):
        for field_name in self.fields:
            self.fields[field_name].help_text = None

    def set_custom_fields(self, form_type):
        if form_type == 'reg':
            # self.fields['gender'].initial = 'do not show'

            self.fields['password1'].widget = forms.PasswordInput(
                attrs={
                    'placeholder': 'Enter password',
                    'class': 'w3-input',
                }
            )
            self.fields['password2'].widget = forms.PasswordInput(
                attrs={
                    'placeholder': 'Confirm password',
                    'class': 'w3-input',
                }
            )
        else:
            self.fields['username'].widget = forms.EmailInput(
                attrs={
                    'placeholder': 'Email',
                    'class': 'w3-input',
                }
            )
            self.fields['password'].widget = forms.PasswordInput(
                attrs={
                    'placeholder': 'Password',
                    'class': 'w3-input',
                }
            )


class ReloadSamePageMixin:
    def get_same_url(self):
        post_pk = self.kwargs['pk']
        page_pk = self.kwargs['page']
        return reverse_lazy('post-details-comments', kwargs={'pk': int(post_pk), 'page': int(page_pk)})


def save_liking(req, pk, CurrentObject):
    exists = CurrentObject.objects.filter(
        post_id=pk,
        owner_id=req.user.pk,
    )
    if exists:
        return exists.delete()

    obj = CurrentObject(
        post=Post.objects.get(pk=pk),
        owner=req.user,
    )
    obj.save()


def check_opposite_liking_exists(req, pk, CurrentObject):
    obj = CurrentObject.objects.filter(
        post_id=pk,
        owner_id=req.user.pk,
    )
    if obj:
        obj.delete()


class LoadCommentsContextDataMixin:
    def load_ctx(self, ctx):
        post_pk = self.kwargs['pk']
        post = Post.objects.get(pk=post_pk)
        filtered_comments = Comment.objects.select_related('post').filter(post_id=post).order_by('-created')

        paginator = Paginator(filtered_comments, per_page=3)
        page = self.kwargs['page']
        ctx['object_list'] = paginator.get_page(int(page))
        ctx['post_pk'] = post_pk
