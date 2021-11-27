from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from flashcards.models import Question
from flashcards.models import Score
from flashcards.models import Session
from flashcards.views import create_session
from flashcards.views import generate_questions
from random import randint
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient


MOCK_SESSION_ALL = {
    "include_trees": True,
    "include_shrubs": True,
    "include_herbs": True,
    "include_lichens": True,
    "include_poisonous": True,
    "include_colorado": True,
    "include_montana": True,
    "include_new_mexico": True,
    "include_idaho": True,
    "include_utah": True,
    "include_washington": True,
    "include_wyoming": True,
    "total_questions": 5,
}


class TestFlashcards(TestCase):
    fixtures = ["rmf/fixtures/data.yaml"]

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username="testuser", password="12345")
        factory = APIRequestFactory()
        request = factory.post("/flashcards/")
        request.user = user
        for i in range(3):
            Score.objects.create(user=user, date=datetime.now(), score=randint(0, 100))
        self.session = create_session(request, MOCK_SESSION_ALL)
        generate_questions(MOCK_SESSION_ALL, self.session)

    def test_all_scores(self):
        scores = Score.objects.all()
        response = self.client.get(reverse("flashcards:scores"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for score in scores:
            assert score in response.data.serializer.instance

    def test_get_all_sessions(self):
        sessions = Session.objects.all()
        response = self.client.get(reverse("flashcards:sessions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for session in sessions:
            assert session in response.data.serializer.instance

    def test_get_session(self):
        session = Session.objects.filter(pk=self.session.pk)[0]
        response = self.client.get(
            reverse("flashcards:session", args=(self.session.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert session == response.data.serializer.instance

    def test_get_all_questions(self):
        questions = Question.objects.all()
        response = self.client.get(reverse("flashcards:questions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for question in questions:
            assert question in response.data.serializer.instance

    def test_get_question(self):
        pk = 1
        question = Question.objects.filter(pk=pk)[0]
        response = self.client.get(reverse("flashcards:question", args=(pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert question == response.data.serializer.instance
