from django.urls import path

from auth_api.views.forgot_password import ForgotPasswordView
from auth_api.views.login import LoginView
from auth_api.views.register import RegisterUsersView
from auth_api.views.user_details import UserDetailView

urlpatterns = [
    path("register", RegisterUsersView.as_view(), name="Register"),
    path("login", LoginView.as_view(), name="Login"),
    path("user_details", UserDetailView.as_view(), name="User Details"),
    path("forgot_password", ForgotPasswordView.as_view(), name="Forgot Password"),
]