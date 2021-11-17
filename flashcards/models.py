from django.db import models
from django.conf import settings
from library.models import Image


class Session(models.Model):
    session_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Types of plants to include
    include_trees = models.BooleanField(default=True)
    include_shrubs = models.BooleanField(default=True)
    include_herbs = models.BooleanField(default=True)
    include_lichens = models.BooleanField(default=True)
    include_poisonous = models.BooleanField(default=True)
    # Regions to include
    include_colorado = models.BooleanField(default=True)
    include_idaho = models.BooleanField(default=True)
    include_montana = models.BooleanField(default=True)
    include_new_mexico = models.BooleanField(default=True)
    include_utah = models.BooleanField(default=True)
    include_washington = models.BooleanField(default=True)
    include_wyoming = models.BooleanField(default=True)
    # Score
    total_questions = models.IntegerField(default=20)
    num_correct = models.IntegerField(default=0)
    curr_position = models.IntegerField(default=0)

    def __str__(self):
        return str(self.session_user)


class Question(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    plant_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=100)
    choice_a = models.CharField(max_length=100)
    choice_b = models.CharField(max_length=100)
    choice_c = models.CharField(max_length=100)
    choice_d = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.session) + "_" + self.question_name


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
