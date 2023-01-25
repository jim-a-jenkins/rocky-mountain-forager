from django.db.models import Q, QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from flashcards.forms import SessionForm
from flashcards.models import Session, Question, Score
from library.models import Plant, Image
from flashcards.serializers import ScoreSerializer
from flashcards.serializers import SessionSerializer
from flashcards.serializers import QuestionSerializer
from rest_framework import generics, permissions
from typing import Dict, List, Union
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

import random


class Flashcards(View):
    flashcards_form = "flashcards_form.html"
    flashcards_menu = "flashcards_menu.html"
    form_class = SessionForm

    def get(self, request: HttpRequest) -> HttpResponse:
        session_in_progress = (
            len(Session.objects.filter(session_user_id=request.user.id)) != 0
        )
        if session_in_progress:
            session = Session.objects.filter(session_user=request.user)[0]
            return render(request, self.flashcards_menu, {"session": session})
        else:
            form = self.form_class
        return render(request, self.flashcards_form, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
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

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        session_id = kwargs.get("session_id")
        session = Session.objects.filter(session_id=session_id)[0]
        questions = Question.objects.filter(session_id=session_id)
        return render(
            request,
            self.game_template,
            {"question": questions[session.curr_position]},
        )

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
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


def generate_questions(cd: Dict[str, Union[bool, int]], session: Session) -> None:
    counter = 0
    exclude_groups = get_excluded_groups(cd)
    region_kwargs = get_excluded_regions(cd)
    plants = Plant.objects.filter(Q(**region_kwargs, _connector=Q.OR))
    for group in exclude_groups:
        plants = plants.exclude(group__exact=group)
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
                other_options.extend(extra_options_names)
                other_options = [*set(other_options)] # remove duplicates
            for key, _ in choices.items():
                if choices[key] is None:
                    try_again = True
                    while try_again is True:
                        choice = random.choice(other_options)
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


def create_session(request: HttpRequest, cd: Dict[str, Union[bool, int]]):
    session = Session.objects.create(
        include_trees=cd["include_trees"],
        include_shrubs=cd["include_shrubs"],
        include_herbs=cd["include_herbs"],
        include_lichens=cd["include_lichens"],
        include_poisonous=cd["include_poisonous"],
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


def get_excluded_groups(data: Dict[str, Union[bool, int]]) -> List[str]:
    exclude_groups: List[str] = []
    if data["include_trees"] is False:
        exclude_groups.append('Trees')
    if data["include_shrubs"] is False:
        exclude_groups.append('Shrubs')
    if data["include_herbs"] is False:
        exclude_groups.append('Herbs')
    if data["include_lichens"] is False:
        exclude_groups.append('Lichens')
    if data["include_poisonous"] is False:
        exclude_groups.append('Poisonous')
    return exclude_groups


def get_excluded_regions(data: Dict[str, Union[bool, int]]) -> Dict[str, bool]:
    region_kwargs: Dict[str, bool] = {}
    if data["include_colorado"]:
        region_kwargs["in_colorado"] = True
    if data["include_idaho"]:
        region_kwargs["in_idaho"] = True
    if data["include_montana"]:
        region_kwargs["in_montana"] = True
    if data["include_new_mexico"]:
        region_kwargs["in_new_mexico"] = True
    if data["include_utah"]:
        region_kwargs["in_utah"] = True
    if data["include_washington"]:
        region_kwargs["in_washington"] = True
    if data["include_wyoming"]:
        region_kwargs["in_wyoming"] = True
    return region_kwargs


def get_extra_options_names(plants: QuerySet[Plant]):
    """
    In the case where the filters don't return enough plants for a minimum of 4 multiple choice questions
    grab other options based on plant type of the first plant
    """
    # TODO: fix bug where not enough options 
    first_plant = plants[0]
    extra_options = Plant.objects.filter(
        group=first_plant.group,# not sure about this
        # trees=first_plant.group,
        # shrubs=first_plant.group,
        # lichens=first_plant.group,
        # herbs=first_plant.group,
    )
    extra_options_names = [option.name for option in extra_options]
    return extra_options_names

# API

def generate_questions_api(data: Dict[str, Union[bool, int]], session_id) -> None:
    counter = 0
    exclude_groups = get_excluded_groups(data)
    region_kwargs = get_excluded_regions(data)#TODO update - function doesn't do what it says it does
    plants = Plant.objects.filter(Q(**region_kwargs, _connector=Q.OR))
    for group in exclude_groups:
        plants = plants.exclude(group__exact=group)
    extra_options_names = None
    if len(plants) < 4:
        extra_options_names = get_extra_options_names(plants)
    plant_names = [plant.name for plant in plants]
    while counter < data["total_questions"]:
        random.shuffle(plant_names)
        for plant in plant_names:
            if counter == data["total_questions"]:
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
                other_options.extend(extra_options_names)
                other_options = [*set(other_options)] # remove duplicates
            for key, _ in choices.items():
                if choices[key] is None:
                    try_again = True
                    while try_again is True:
                        choice = random.choice(other_options)
                        if choice != answer and choice in other_options:
                            choices[key] = choice
                            other_options.remove(choice)
                            try_again = False
            Question.objects.create(
                session_id=session_id,
                plant_image=image,
                question_name=str(session_id) + f"_{counter}",
                choice_a=choices["a"],
                choice_b=choices["b"],
                choice_c=choices["c"],
                choice_d=choices["d"],
                answer=answer,
            )
            counter += 1


def create_session_api(user_id: int, data: Dict[str, Union[bool, int]]):
    session = Session.objects.create(
        include_trees=data["include_trees"],
        include_shrubs=data["include_shrubs"],
        include_herbs=data["include_herbs"],
        include_lichens=data["include_lichens"],
        include_poisonous=data["include_poisonous"],
        include_colorado=data["include_colorado"],
        include_idaho=data["include_idaho"],
        include_montana=data["include_montana"],
        include_new_mexico=data["include_new_mexico"],
        include_utah=data["include_utah"],
        include_washington=data["include_washington"],
        include_wyoming=data["include_wyoming"],
        total_questions=data["total_questions"],
        session_user_id=user_id,
    )
    return session

class QuestionsListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScoresListAPIView(generics.ListAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScoreDestroyAPIView(generics.DestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]


class SessionsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    class SessionExistsException(APIException):
        status_code = 400
        default_detail = 'A session already exists for this user.'
    
    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(session_user=user)
    
    def perform_create(self, serializer):
        session = Session.objects.filter(session_user_id=self.request.user.id).first()
        if session:
            raise self.SessionExistsException
        else:
            if serializer.is_valid():
                session = serializer.save(
                    session_user=self.request.user,
                    include_trees=self.request.data.get("include_trees"),
                    include_shrubs=self.request.data.get("include_shrubs"),
                    include_herbs=self.request.data.get("include_herbs"),
                    include_lichens=self.request.data.get("include_lichens"),
                    include_poisonous=self.request.data.get("include_poisonous"),
                    include_colorado=self.request.data.get("include_colorado"),
                    include_idaho=self.request.data.get("include_idaho"),
                    include_montana=self.request.data.get("include_montana"),
                    include_new_mexico=self.request.data.get("include_new_mexico"),
                    include_utah=self.request.data.get("include_utah"),
                    include_washington=self.request.data.get("include_washington"),
                    include_wyoming=self.request.data.get("include_wyoming"),
                    total_questions=self.request.data.get("total_questions")
                )
                generate_questions_api(self.request.data, session.session_id)
                return Response(session.session_id, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SessionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(session_user=user)