from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from flashcards.forms import SessionForm
from flashcards.models import Session, Question, Score
from library.models import Plant, Image
from flashcards.serializers import ScoreSerializer
from flashcards.serializers import SessionSerializer
from flashcards.serializers import QuestionSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import random


class Flashcards(View):
    flashcards_form = "flashcards_form.html"
    flashcards_menu = "flashcards_menu.html"
    form_class = SessionForm

    def get(self, request, *args, **kwargs):
        session_in_progress = (
            len(Session.objects.filter(session_user_id=request.user.id)) != 0
        )
        if session_in_progress:
            session = Session.objects.filter(session_user=request.user)[0]
            return render(request, self.flashcards_menu, {"session": session})
        else:
            form = self.form_class
        return render(request, self.flashcards_form, {"form": form})

    def post(self, request, *args, **kwargs):
        session_in_progress = (
            len(Session.objects.filter(session_user_id=request.user.id)) != 0
        )
        if session_in_progress:
            session = Session.objects.filter(session_user=request.user)[0]
            if request.POST.get("choice") == "Continue Session":
                return HttpResponseRedirect(str(session.session_id))
            else:
                Session.objects.filter(session_user=session.session_user).delete()
                form = self.form_class
                return render(request, self.flashcards_form, {"form": form})
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                session = create_session(request, cd)
                generate_questions(cd, session)
                return HttpResponseRedirect(str(session.session_id))
            else:
                return HttpResponse("Failed to create flashcards session")


class Game(View):
    answer_template = "answer.html"
    game_template = "game.html"
    score_template = "score.html"

    def get(self, request, *args, **kwargs):
        session_id = kwargs.get("session_id")
        session = Session.objects.filter(session_id=session_id)[0]
        questions = Question.objects.filter(session_id=session_id)
        return render(
            request,
            self.game_template,
            {"question": questions[session.curr_position]},
        )

    def post(self, request, *args, **kwargs):
        session_id = kwargs.get("session_id")
        session = Session.objects.filter(session_id=session_id)[0]
        if (
            request.POST.get("next")
            and session.curr_position == session.total_questions
        ):
            Session.objects.filter(session_user=session.session_user).delete()
            score = session.num_correct * 100 // session.total_questions
            Score.objects.create(user=session.session_user, score=score)
            return render(
                request,
                self.score_template,
                {
                    "num_correct": session.num_correct,
                    "total_questions": session.total_questions,
                    "score": score,
                },
            )
        elif request.POST.get("next"):
            questions = Question.objects.filter(session_id=session_id)
            Session.objects.filter(session_user=request.user).update(
                curr_position=session.curr_position
            )
            return render(
                request,
                self.game_template,
                {"question": questions[session.curr_position]},
            )
        else:
            question_name = str(session_id) + "_" + str(session.curr_position)
            question = Question.objects.filter(question_name__exact=question_name)[0]
            correct_answer = request.POST.get("choice") == question.answer
            if correct_answer:
                session.num_correct += 1
            session.curr_position += 1
            Session.objects.filter(session_user=request.user).update(
                num_correct=session.num_correct, curr_position=session.curr_position
            )
            return render(
                request,
                self.answer_template,
                {"correct_answer": correct_answer, "question": question},
            )


def generate_questions(cd, session):
    counter = 0
    exclude_kwargs = get_excluded_groups(cd)
    region_kwargs = get_excluded_regions(cd)
    plants = Plant.objects.filter(Q(**region_kwargs, _connector=Q.OR)).exclude(
        Q(**exclude_kwargs, _connector=Q.OR)
    )
    extra_options_names = None
    if len(plants) < 4:
        extra_options_names = get_extra_options_names(plants)
    plant_names = [plant.name for plant in plants]
    while counter < cd["total_questions"]:
        random.shuffle(plant_names)
        for plant in plant_names:
            if counter == cd["total_questions"]:
                break
            images = Image.objects.filter(plant__name__exact=plant)
            image = images[random.randint(0, len(images) - 1)]
            image.__setattr__("image_name", image.__str__())
            answer = plant
            choices = {"a": None, "b": None, "c": None, "d": None}
            answer_choice = random.choice(list(choices))
            choices[answer_choice] = answer
            other_options = plant_names.copy()
            if extra_options_names:
                other_options.append(extra_options_names)
            for key, value in choices.items():
                if choices[key] is None:
                    try_again = True
                    while try_again is True:
                        choice = random.choice(plant_names)
                        if choice != answer and choice in other_options:
                            choices[key] = choice
                            other_options.remove(choice)
                            try_again = False
            Question.objects.create(
                session_id=session.session_id,
                plant_image=image,
                question_name=str(session.session_id) + f"_{counter}",
                choice_a=choices["a"],
                choice_b=choices["b"],
                choice_c=choices["c"],
                choice_d=choices["d"],
                answer=answer,
            )
            counter += 1


def create_session(request, cd):
    session = Session.objects.create(
        include_trees=cd["include_trees"],
        include_shrubs=cd["include_shrubs"],
        include_colorado=cd["include_colorado"],
        include_idaho=cd["include_idaho"],
        include_montana=cd["include_montana"],
        include_new_mexico=cd["include_new_mexico"],
        include_utah=cd["include_utah"],
        include_washington=cd["include_washington"],
        include_wyoming=cd["include_wyoming"],
        total_questions=cd["total_questions"],
        session_user_id=request.user.id,
    )
    return session


def get_excluded_groups(cd):
    exclude_kwargs = {}
    if cd["include_trees"] is False:
        exclude_kwargs["trees"] = True
    if cd["include_shrubs"] is False:
        exclude_kwargs["shrubs"] = True
    if cd["include_herbs"] is False:
        exclude_kwargs["herbs"] = True
    if cd["include_lichens"] is False:
        exclude_kwargs["lichens"] = True
    if cd["include_poisonous"] is False:
        exclude_kwargs["poisonous"] = True
    return exclude_kwargs


def get_excluded_regions(cd):
    region_kwargs = {}
    if cd["include_colorado"]:
        region_kwargs["in_colorado"] = True
    if cd["include_idaho"]:
        region_kwargs["in_idaho"] = True
    if cd["include_montana"]:
        region_kwargs["in_montana"] = True
    if cd["include_new_mexico"]:
        region_kwargs["in_new_mexico"] = True
    if cd["include_utah"]:
        region_kwargs["in_utah"] = True
    if cd["include_washington"]:
        region_kwargs["in_washington"] = True
    if cd["include_wyoming"]:
        region_kwargs["in_wyoming"] = True
    return region_kwargs


def get_extra_options_names(plants):
    """
    In the case where the filters don't return enough plants for a minimum of 4 multiple choice questions
    grab other options based on plant type of the first plant
    """
    first_plant = plants[0]
    extra_options = Plant.objects.filter(
        trees=first_plant.trees,
        shrubs=first_plant.shrubs,
        lichens=first_plant.lichens,
        herbs=first_plant.herbs,
    )
    extra_options_names = [option.name for option in extra_options]
    return extra_options_names


@api_view(["GET"])
def scores(request):
    if request.method == "GET":
        scores = Score.objects.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def sessions(request):
    if request.method == "GET":
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            "session_id": request.data.get("session_id"),
            "session_user": request.data.get("session_user"),
            "include_trees": request.data.get("include_trees"),
            "include_shrubs": request.data.get("include_shrubs"),
            "include_herbs": request.data.get("include_herbs"),
            "include_lichens": request.data.get("include_lichens"),
            "include_poisonous": request.data.get("include_poisonous"),
            "include_colorado": request.data.get("include_colorado"),
            "include_idaho": request.data.get("include_idaho"),
            "include_montana": request.data.get("include_montana"),
            "include_new_mexico": request.data.get("include_new_mexico"),
            "include_utah": request.data.get("include_utah"),
            "include_washington": request.data.get("include_washington"),
            "include_wyoming": request.data.get("include_wyoming"),
            "total_questions": request.data.get("total_questions"),
            "num_correct": request.data.get("num_correct"),
            "curr_position": request.data.get("curr_position"),
        }
        serializer = SessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def session(request, session_id):
    try:
        session = Session.objects.get(session_id=session_id)
    except Session.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SessionSerializer(session)
        return Response(serializer.data)


@api_view(["GET"])
def questions(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def question(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
