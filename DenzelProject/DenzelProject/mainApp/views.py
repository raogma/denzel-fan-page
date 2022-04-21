from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class ContactsView(LoginRequiredMixin, TemplateView,):
    template_name = 'contacts.html'


class WelcomeView(TemplateView):
    template_name = 'welcome.html'

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            return redirect('posts')
        return res


def not_found_view(request, exception):
    return render(request, 'page404.html')


class NotFoundView(TemplateView):
    template_name = 'page404.html'

# class SuccessView(LoginRequiredMixin, TemplateView):
#     template_name = 'success.html'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     ctx['action'] = self.request.get('url')
    #     return ctx
