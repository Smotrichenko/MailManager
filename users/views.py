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
            reverse("confirm_email", kwargs={"uidb64": uid, "token": token})
        )

        send_mail(
            subject="Подтверждение регистрации.",
            message=f"Подтвердите email по ссылке: {confirm_url}.",
            from_email=None,
            recipient_list=[user.email],
        )

        messages.success(request, "Письмо подтверждения отправлено на email.")
        return redirect("login")


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields["is_active"])
            messages.success(request, "Email подтверждён, войдите в систему.")
            return redirect("login")

        messages.error(request, "Ссылка подтверждения недействительна.")
        return redirect("login")
