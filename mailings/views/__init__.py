from .mailings import (HomeView, MailingsCreateView, MailingsDeleteView,
                       MailingsDetailView, MailingsListView,
                       MailingsUpdateView, send_mailing_view)
from .manager import ToggleMailingEnabledView
from .message import (MessageCreateView, MessageDeleteView, MessageListView,
                      MessageUpdateView)
from .recipients import (RecipientCreateView, RecipientDeleteView,
                         RecipientListView, RecipientUpdateView)
from .stats import StatsView
