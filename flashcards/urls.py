from django.urls import path
from .views import Flashcards, Game

app_name = "flashcards"

urlpatterns = [
    path("flashcards/", Flashcards.as_view(), name="flashcards"),
    path("flashcards/<uuid:session_id>", Game.as_view(), name="game"),
]
