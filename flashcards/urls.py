from django.urls import path
from flashcards.views import Flashcards, Game
from flashcards.views import QuestionsListAPIView
from flashcards.views import QuestionRetrieveAPIView
from flashcards.views import ScoresListAPIView
from flashcards.views import SessionsListCreateAPIView
from flashcards.views import SessionRetrieveUpdateDestroyAPIView


app_name = "flashcards"

urlpatterns = [
    path("flashcards/", Flashcards.as_view(), name="flashcards"),
    path("flashcards/<uuid:session_id>", Game.as_view(), name="game"),
    # api
    path("api/v1/questions/", QuestionsListAPIView.as_view(), name="questions"),
    path("api/v1/questions/<int:pk>", QuestionRetrieveAPIView.as_view(), name="question"),
    path("api/v1/scores/", ScoresListAPIView.as_view(), name="scores"),
    path("api/v1/sessions/", SessionsListCreateAPIView.as_view(), name="sessions"),
    path("api/v1/sessions/<uuid:pk>", SessionRetrieveUpdateDestroyAPIView.as_view(), name="session"),
]
