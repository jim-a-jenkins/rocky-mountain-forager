from rest_framework import serializers
from flashcards.models import Score
from flashcards.models import Session
from flashcards.models import Question


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = (
            "id",
            "user",
            "date",
            "score",
        )


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = (
            "session_id",
            "session_user",
            "include_trees",
            "include_shrubs",
            "include_herbs",
            "include_lichens",
            "include_poisonous",
            "include_colorado",
            "include_idaho",
            "include_montana",
            "include_new_mexico",
            "include_utah",
            "include_washington",
            "include_wyoming",
            "total_questions",
            "num_correct",
            "curr_position",
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "session",
            "plant_image",
            "question_name",
            "choice_a",
            "choice_b",
            "choice_c",
            "choice_d",
            "answer",
        )


