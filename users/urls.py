from config.urls import path
from mailings.urls import app_name
from users.views import RegisterView, ConfirmEmailView
from django.contrib.auth import views as auth_views

from users.views_manager import UserListView, ToggleUserBlockView


app_name = "users"

urlpatterns = [
    # Регистрация + подтверждение
    path("register/", RegisterView.as_view(), name="register"),
    path("confirm/<uidb64>/<token>/", ConfirmEmailView.as_view(), name="confirm_email"),

    # Вход/выход
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("all/", UserListView.as_view(), name="user_list"),
    path("all/<int:pk>/toggle-block/", ToggleUserBlockView.as_view(), name="user_toggle_block"),

    # Восстановление пароля
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
