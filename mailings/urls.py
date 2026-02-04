from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import (HomeView, MailingsCreateView, MailingsDeleteView,
                            MailingsDetailView, MailingsListView,
                            MailingsUpdateView, MessageCreateView,
                            MessageDeleteView, MessageListView,
                            MessageUpdateView, RecipientCreateView,
                            RecipientDeleteView, RecipientListView,
                            RecipientUpdateView, send_mailing_view)
from mailings.views_manager import ToggleMailingEnabledView

app_name = MailingsConfig.name


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipients/<int:pk>/edit/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailings/", MailingsListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingsCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/", MailingsDetailView.as_view(), name="mailing_detail"),
    path(
        "mailings/<int:pk>/edit/", MailingsUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailings/<int:pk>/delete/", MailingsDeleteView.as_view(), name="mailing_delete"
    ),
    path("mailings/<int:pk>/send/", send_mailing_view, name="mailing_send"),
    path(
        "mailings/<int:pl>/toggle-enabled",
        ToggleMailingEnabledView.as_view(),
        name="mailing_toggle_enabled",
    ),
]
