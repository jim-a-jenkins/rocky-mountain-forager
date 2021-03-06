# Generated by Django 3.2.8 on 2021-11-20 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "session_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("include_trees", models.BooleanField(default=True)),
                ("include_shrubs", models.BooleanField(default=True)),
                ("include_herbs", models.BooleanField(default=True)),
                ("include_lichens", models.BooleanField(default=True)),
                ("include_poisonous", models.BooleanField(default=True)),
                ("include_colorado", models.BooleanField(default=True)),
                ("include_idaho", models.BooleanField(default=True)),
                ("include_montana", models.BooleanField(default=True)),
                ("include_new_mexico", models.BooleanField(default=True)),
                ("include_utah", models.BooleanField(default=True)),
                ("include_washington", models.BooleanField(default=True)),
                ("include_wyoming", models.BooleanField(default=True)),
                ("total_questions", models.IntegerField(default=20)),
                ("num_correct", models.IntegerField(default=0)),
                ("curr_position", models.IntegerField(default=0)),
                (
                    "session_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Score",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("score", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_name", models.CharField(max_length=100)),
                ("choice_a", models.CharField(max_length=100)),
                ("choice_b", models.CharField(max_length=100)),
                ("choice_c", models.CharField(max_length=100)),
                ("choice_d", models.CharField(max_length=100)),
                ("answer", models.CharField(max_length=100)),
                (
                    "plant_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.image"
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="flashcards.session",
                    ),
                ),
            ],
        ),
    ]
