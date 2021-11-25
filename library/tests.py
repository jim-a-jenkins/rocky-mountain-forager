from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from library.models import Plant
from rest_framework.test import APIClient


class TestSession(TestCase):
    fixtures = ["rmf/fixtures/data.yaml"]

    def setUp(self):
        self.client = APIClient()

    def test_all_plants(self):
        plants = Plant.objects.all()
        response = self.client.get(reverse("library:plants"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for plant in plants:
            assert plant in response.data.serializer.instance

    def test_get_plant(self):
        pk = 1
        plant = Plant.objects.filter(pk=pk)[0]
        response = self.client.get(reverse("library:plant", args=(pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert plant == response.data.serializer.instance
