from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from flashcards.models import Score
from library.forms import UserRegistrationForm
from library.models import Image, Plant
from library.serializers import ImageSerializer, PlantSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


def library(request):
    trees = Plant.objects.filter(trees=True, poisonous=False)
    shrubs = Plant.objects.filter(shrubs=True, poisonous=False)
    poisonous_lookalikes = Plant.objects.filter(poisonous=True)
    return render(
        request,
        "library.html",
        context={
            "trees": trees,
            "shrubs": shrubs,
            "poisonous_lookalikes": poisonous_lookalikes,
        },
    )


def plant_detail(request, plant):
    plant = get_object_or_404(Plant, slug=plant)
    images = Image.objects.filter(plant__name__exact=plant.name)
    return render(request, "plant.html", context={"plant": plant, "images": images})


@login_required
def account(request):
    scores = Score.objects.all()
    return render(request, "account.html", {"scores": scores})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, "register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "register.html", {"user_form": user_form})


@api_view(["GET"])
def images(request):
    if request.method == "GET":
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def image(request, pk):
    try:
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ImageSerializer(image)
        return Response(serializer.data)


@api_view(["GET"])
def plants(request):
    if request.method == "GET":
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def plant(request, pk):
    try:
        plant = Plant.objects.get(pk=pk)
    except Plant.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = PlantSerializer(plant)
        return Response(serializer.data)
