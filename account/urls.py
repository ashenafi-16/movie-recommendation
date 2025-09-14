from django.urls import path
from .views import (
    RegisterView,
    LoginView,
)
from .base.csrf import CSFRAPIView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-user'),
    path('csrf_token/', CSFRAPIView.as_view(), name='csrf-token'),
    path('login/', LoginView.as_view(), name='login'),
]