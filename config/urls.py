from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mailings.urls", namespace="mailings")),
    path("users/", include("users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
