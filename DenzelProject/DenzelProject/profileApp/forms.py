from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from DenzelProject.profileApp.models import Profile
from DenzelProject.utils import ApplyStyleMixin


class CreateProfileForm(UserCreationForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_w3()
        self.set_labels()
        self.remove_help_text()
        self.set_custom_fields('reg')

    # def save(self, commit=True):
    #     user = super().save(commit=commit)
    #     profile = Profile(
    #         first_name=self.cleaned_data['first_name'],
    #         last_name=self.cleaned_data['last_name'],
    #         avatar=self.cleaned_data['avatar'],
    #         gender=self.cleaned_data['gender'],
    #         phone_number=self.cleaned_data['phone_number'],
    #         user=user,
    #     )
    #     if commit:
    #         profile.save()
    #     return user
    #
    # gender_choices = [
    #     'male', 'female', 'do not show',
    # ]
    # avatar = forms.FileField(
    #     widget=forms.FileInput(),
    #     required=False,
    # )
    # first_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder': 'First name',
    #         },
    #     )
    # )
    # last_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder': 'Last name',
    #         },
    #     )
    # )
    # address = forms.CharField(
    #     max_length=40,
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder': 'Address',
    #         },
    #     )
    # )
    # phone_number = forms.IntegerField(
    #     required=False,
    #     widget=forms.NumberInput(
    #         attrs={
    #             'placeholder': 'Phone number',
    #         },
    #     )
    # )
    #
    # gender = forms.ChoiceField(
    #     required=False,
    #     choices=[(x, x) for x in gender_choices],
    # )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email'
                }
            ),
        }


class EditProfileForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_w3()
        self.set_labels()

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'avatar': AdminFileWidget(),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name'
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name'
                },
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'placeholder': 'Phone Number'
                },
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Address'
                },
            ),
        }


class DeleteProfileForm(forms.ModelForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_w3()
        self.set_labels()
        self.disable_fields()

    class Meta:
        model = Profile
        exclude = ('user', )
        widgets = {
            'avatar': AdminFileWidget(),
        }


class LoginForm(AuthenticationForm, ApplyStyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_w3()
        self.set_labels()
        self.set_custom_fields('login')

    class Meta:
        model = get_user_model()
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Email'
                },
            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Password'
                },
            )
        }
