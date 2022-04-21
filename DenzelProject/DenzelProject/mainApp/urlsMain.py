from django.urls import path

from DenzelProject.blogPost.views import DashView
from DenzelProject.mainApp.views import ContactsView, WelcomeView

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('', WelcomeView.as_view(), name='welcome'),
    # path('success/', SuccessView.as_view(), name='success'),

]
