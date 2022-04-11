from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, DeleteView

from DenzelProject.blogPost.models import Post
from DenzelProject.profileApp.forms import CreateProfileForm, LoginForm, EditProfileForm, DeleteProfileForm
from DenzelProject.profileApp.models import Profile


class ProfileDetails(LoginRequiredMixin, DetailView):
    template_name = 'profile/profile-details.html'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_posts = Post.objects.select_related('owner').filter(owner_id=self.object.pk)
        ctx['user_posts'] = user_posts

        likes = sum([x.like_set.count() for x in user_posts])
        dislikes = sum([x.dislike_set.count() for x in user_posts])
        total_liking = likes + dislikes
        x = 0
        if total_liking != 0:
            x = round(likes * 100 / total_liking)
        ctx['liking_percent'] = x

        return ctx


class RegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'profile/create-profile.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form = super().form_valid(form)
        login(self.request, self.object)
        return form


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'profile/edit-profile.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.user_id})


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = Profile
    form_class = DeleteProfileForm
    template_name = 'profile/delete-profile.html'

    def get_success_url(self):
        return reverse_lazy('welcome')

    def get_initial(self):
        return {
            'avatar': self.object.avatar,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'phone_number': self.object.phone_number,
            'address': self.object.address,
            'gender': self.object.gender
        }


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'profile/login.html'

    def get_success_url(self):
        return reverse_lazy('posts')


class LogoutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/logout.html'


class LogoutConfirmView(LoginRequiredMixin, LogoutView):
    def get_next_page(self):
        return reverse_lazy('welcome')
