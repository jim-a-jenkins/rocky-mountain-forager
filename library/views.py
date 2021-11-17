from django.shortcuts import render, get_object_or_404
from .models import Plant, Image
from flashcards.models import Score
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


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
