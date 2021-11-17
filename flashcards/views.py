from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import SessionForm
from .models import Session, Question, Score
from library.models import Plant, Image
import random


class Flashcards(View):
    game_template = 'game.html'
    flashcards_template = 'flashcards.html'
    score_template = 'score.html'
    answer_template = 'answer.html'
    form_class = SessionForm

    def get(self, request, *args, **kwargs):
        session_in_progress = len(Session.objects.filter(session_user_id=request.user.id)) != 0
        if session_in_progress:
            session = Session.objects.filter(session_user=request.user)[0]
            question_name = str(session.id) + '_' + str(session.curr_position)
            question = Question.objects.filter(question_name__exact=question_name)[0]
            return render(request, self.game_template, {'session': session, 'question': question})
        else:
            form = self.form_class
        return render(request, self.flashcards_template, {'form': form})

    def post(self, request, *args, **kwargs):
        session_in_progress = len(Session.objects.filter(session_user_id=request.user.id)) != 0
        if session_in_progress:
            session = Session.objects.filter(session_user=request.user)[0]
            if request.POST.get('next') and session.curr_position == session.total_questions - 1:
                Session.objects.filter(session_user=session.session_user).delete()
                score = session.num_correct * 100 // session.total_questions
                Score.objects.create(user=session.session_user, score=score)
                return render(request, self.score_template, {'num_correct': session.num_correct,
                                                      'total_questions': session.total_questions,
                                                      'score': score})
            elif request.POST.get('next'):
                session.curr_position += 1
                questions = Question.objects.filter(session_id=session.id)
                Session.objects.filter(session_user=request.user).update(curr_position=session.curr_position)
                return render(request, self.game_template, {'question': questions[session.curr_position]})
            else:
                question_name = str(session.id) + '_' + str(session.curr_position)
                question = Question.objects.filter(question_name__exact=question_name)[0]
                correct_answer = request.POST.get('choice') == question.answer
                if correct_answer:
                    session.num_correct += 1
                Session.objects.filter(session_user=request.user).update(num_correct=session.num_correct)
                return render(request, self.answer_template, {'correct_answer': correct_answer, 'question': question})
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                session = create_session(request, cd)
                generate_questions(cd, session)
                questions = Question.objects.filter(session_id=session.id)
                return render(request, self.game_template, {'session': session, 'question': questions[0]})
            else:
                return HttpResponse('Failed to create flashcards session')


def generate_questions(cd, session):
    counter = 0
    exclude_kwargs = get_excluded_groups(cd)
    region_kwargs = get_excluded_regions(cd)
    plants = Plant.objects.filter(Q(**region_kwargs, _connector=Q.OR)).exclude(Q(**exclude_kwargs, _connector=Q.OR))
    extra_options_names = None
    if len(plants) < 4:
        extra_options_names = get_extra_options_names(plants)
    plant_names = [plant.name for plant in plants]
    while counter < cd['total_questions']:
        random.shuffle(plant_names)
        for plant in plant_names:
            if counter == cd['total_questions']:
                break
            images = Image.objects.filter(plant__name__exact=plant)
            image = images[random.randint(0, len(images) - 1)]
            image.__setattr__('image_name', image.__str__())
            answer = plant
            choices = {'a': None, 'b': None, 'c': None, 'd': None}
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
            Question.objects.create(session_id=session.id,
                                    plant_image=image,
                                    question_name=str(session.id) + f'_{counter}',
                                    choice_a=choices['a'],
                                    choice_b=choices['b'],
                                    choice_c=choices['c'],
                                    choice_d=choices['d'],
                                    answer=answer)
            counter += 1


def create_session(request, cd):
    session = Session.objects.create(include_trees=cd['include_trees'],
                                     include_shrubs=cd['include_shrubs'],
                                     include_colorado=cd['include_colorado'],
                                     include_idaho=cd['include_idaho'],
                                     include_montana=cd['include_montana'],
                                     include_new_mexico=cd['include_new_mexico'],
                                     include_utah=cd['include_utah'],
                                     include_washington=cd['include_washington'],
                                     include_wyoming=cd['include_wyoming'],
                                     total_questions=cd['total_questions'],
                                     session_user_id=request.user.id)
    return session


def get_excluded_groups(cd):
    exclude_kwargs = {}
    if cd['include_trees'] is False:
        exclude_kwargs['trees'] = True
    if cd['include_shrubs'] is False:
        exclude_kwargs['shrubs'] = True
    if cd['include_herbs'] is False:
        exclude_kwargs['herbs'] = True
    if cd['include_lichens'] is False:
        exclude_kwargs['lichens'] = True
    if cd['include_poisonous'] is False:
        exclude_kwargs['poisonous'] = True
    return exclude_kwargs


def get_excluded_regions(cd):
    region_kwargs = {}
    if cd['include_colorado']:
        region_kwargs['in_colorado'] = True
    if cd['include_idaho']:
        region_kwargs['in_idaho'] = True
    if cd['include_montana']:
        region_kwargs['in_montana'] = True
    if cd['include_new_mexico']:
        region_kwargs['in_new_mexico'] = True
    if cd['include_utah']:
        region_kwargs['in_utah'] = True
    if cd['include_washington']:
        region_kwargs['in_washington'] = True
    if cd['include_wyoming']:
        region_kwargs['in_wyoming'] = True
    return region_kwargs


def get_extra_options_names(plants):
    """
    In the case where the filters don't return enough plants for a minimum of 4 multiple choice questions
    grab other options based on plant type of the first plant
    """
    first_plant = plants[0]
    extra_options = Plant.objects.filter(trees=first_plant.trees, shrubs=first_plant.shrubs,
                                         lichens=first_plant.lichens, herbs=first_plant.herbs)
    extra_options_names = [option.name for option in extra_options]
    return extra_options_names
