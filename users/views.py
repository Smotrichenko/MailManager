from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from django.urls import reverse

from users.forms import RegisterForm
from users.models import User


class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirm_url = request.build_absolute_uri(
            reverse("users:confirm_email", kwargs={"uidb64": uid, "token": token})
        )

        send_mail(
            subject="Email confirmation",
            message=f"Confirm your email:\n {confirm_url}.\n",
            from_email=None,
            recipient_list=[user.email],
        )

        messages.success(request, "Письмо подтверждения отправлено на email.")
        return redirect("users:login")


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist, TypeError, OverflowError):
            user = None

        if user is None:
            messages.error(request, "Неверная ссылка подтверждения.")
            return redirect("users:login")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            messages.success(request, "Email подтверждён. Теперь можно войти.")
            return redirect("users:login")

        messages.error(request, "Ссылка подтверждения устарела или неверна.")
        return redirect("users:login")
