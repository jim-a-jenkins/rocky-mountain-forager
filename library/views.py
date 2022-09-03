from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from flashcards.models import Score
from library.forms import UserRegistrationForm
from library.models import Image, Plant
from library.serializers import ImageSerializer, PlantSerializer
from rest_framework import generics


def library(request: HttpRequest) -> HttpResponse:
    trees = Plant.objects.filter(group='Trees', poisonous=False)
    shrubs = Plant.objects.filter(group='Shrubs', poisonous=False)
    herbs = Plant.objects.filter(group='Herbs', poisonous=False)
    lichens = Plant.objects.filter(group='Lichens', poisonous=False)
    poisonous_lookalikes = Plant.objects.filter(poisonous=True)
    return render(
        request,
        "library.html",
        context={
            "trees": trees,
            "shrubs": shrubs,
            "herbs": herbs,
            "lichens": lichens,
            "poisonous_lookalikes": poisonous_lookalikes,
        },
    )


def plant_detail(request: HttpRequest, plant) -> HttpResponse:
    plant = get_object_or_404(Plant, slug=plant)
    images = Image.objects.filter(plant__name__exact=plant.name)
    return render(request, "plant.html", context={"plant": plant, "images": images})


@login_required
def account(request: HttpRequest)  -> HttpResponse:
    scores = Score.objects.all()
    return render(request, "account.html", {"scores": scores})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user: User = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, "register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "register.html", {"user_form": user_form})


#  API

class ImagesListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class PlantsListAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    
    def get_queryset(self):
        queryset = Plant.objects.all()
        group = self.request.query_params.get('group')
        poisonous = self.request.query_params.get('poisonous')
        if group is not None:
            queryset = queryset.filter(group=group)
        if poisonous is not None:
            queryset = queryset.filter(poisonous=poisonous)
        return queryset

class PlantRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
