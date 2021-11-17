from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("flashcards.urls", namespace="flashcards")),
    path("", include("library.urls", namespace="library")),
    path("cookies/", include("cookie_consent.urls")),
]
