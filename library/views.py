from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from flashcards.models import Score
from library.forms import UserRegistrationForm
from library.models import Image, Plant
from library.serializers import ImageSerializer, PlantSerializer
from rest_framework import generics

from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


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

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            user.save()
            
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error': 'The requested username has already been taken. '
                 'Please choose another username.'}, status=400
            )

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(
            request,
            username=data["username"],
            password=data["password"]
        )
        if user is None:
            return JsonResponse(
                {"error": "Invalid credentials. Please check your "
                 "username and password."}, status=400
            )
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)

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
