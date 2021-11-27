from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from library.models import Image
from library.models import Plant
from rest_framework.test import APIClient


class TestLibrary(TestCase):
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

    def test_all_images(self):
        images = Image.objects.all()
        response = self.client.get(reverse("library:images"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for image in images:
            assert image in response.data.serializer.instance

    def test_get_image(self):
        pk = 11
        image = Image.objects.filter(pk=pk)[0]
        response = self.client.get(reverse("library:image", args=(pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert image == response.data.serializer.instance
