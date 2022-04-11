from django.urls import path

from DenzelProject.profileApp.views import ProfileDetails, RegisterView, LoginView, LogoutTemplateView, \
    LogoutConfirmView, EditProfileView, DeleteProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='create-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutTemplateView.as_view(), name='logout'),
    path('logout-confirm/', LogoutConfirmView.as_view(), name='logout-confirm'),
    path('details/<int:pk>/', ProfileDetails.as_view(), name='profile-details'),
    path('edit/<int:pk>', EditProfileView.as_view(), name='edit-profile'),
    path('delete/<int:pk>', DeleteProfileView.as_view(), name='delete-profile'),
]
