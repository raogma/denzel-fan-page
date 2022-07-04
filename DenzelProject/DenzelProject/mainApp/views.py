from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class ContactsView(TemplateView,):
    template_name = 'contacts.html'


class WelcomeView(TemplateView):
    template_name = 'welcome.html'

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            return redirect('posts')
        return res
