from django.urls import path
from flashcards.views import Flashcards, Game
from flashcards.views import question
from flashcards.views import questions
from flashcards.views import scores
from flashcards.views import session
from flashcards.views import sessions

app_name = "flashcards"

urlpatterns = [
    path("flashcards/", Flashcards.as_view(), name="flashcards"),
    path("flashcards/<uuid:session_id>", Game.as_view(), name="game"),
    # api
    path("scores/", scores, name="scores"),
    path("sessions/", sessions, name="sessions"),
    path("sessions/<uuid:session_id>", session, name="session"),
    path("questions/", questions, name="questions"),
    path("questions/<int:pk>", question, name="question"),
]
