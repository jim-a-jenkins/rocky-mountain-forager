from django import forms
from .models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = [
            "include_trees",
            "include_shrubs",
            "include_herbs",
            "include_lichens",
            "include_poisonous",
            "include_colorado",
            "include_montana",
            "include_new_mexico",
            "include_idaho",
            "include_utah",
            "include_washington",
            "include_wyoming",
            "total_questions",
        ]
