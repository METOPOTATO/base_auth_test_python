from django.urls import path

from .views import LoginView, RegisterView, UserDetailView, EmailVerifyView

urlpatterns = [
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/login', LoginView.as_view(), name='login'),
    path('user/detail', UserDetailView.as_view(), name='detail'),
    path('user/email/verify', EmailVerifyView.as_view(), name='verify'),
]
