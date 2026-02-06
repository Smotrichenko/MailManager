from django import forms

from .models import Mailings, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ("owner",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class MailingsForm(forms.ModelForm):
    class Meta:
        model = Mailings
        exclude = ("owner",)
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
