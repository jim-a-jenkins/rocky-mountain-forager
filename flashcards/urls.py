from django.urls import path
from .views import Flashcards

app_name = 'flashcards'

urlpatterns = [
    path('flashcards/', Flashcards.as_view(), name='flashcards'),
]
