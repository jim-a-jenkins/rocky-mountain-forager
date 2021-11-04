from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('flashcards/', views.flashcards, name='flashcards'),
]
