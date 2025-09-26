from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    # fetch_movie,
    LogoutView,
    PasswordChangeView,
    ProfileView,
)
from .password_reset import password_reset, PasswordResetRequestView, PasswordResetConfirmView
from .base.csrf import CSFRAPIView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-user'),
    path('csrf_token/', CSFRAPIView.as_view(), name='csrf-token'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    # path('movie/', fetch_movie, name='fetch_movies'),
    path("profile/", ProfileView.as_view(), name="user-profile"),


    

]
