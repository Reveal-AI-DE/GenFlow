# Generated by Django 5.1.6 on 2025-04-22 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import genflow.apps.assistant.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
        ("team", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Assistant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("is_pinned", models.BooleanField(default=False)),
                ("pre_prompt", models.TextField()),
                ("suggested_questions", models.JSONField(null=True)),
                (
                    "prompt_type",
                    models.CharField(
                        choices=[("simple", "Simple"), ("advanced", "Advanced")],
                        default="simple",
                        max_length=10,
                    ),
                ),
                ("opening_statement", models.TextField(null=True)),
                (
                    "context_source",
                    models.CharField(
                        choices=[("files", "Files"), ("collections", "Collections")],
                        default="files",
                        max_length=25,
                    ),
                ),
                ("collection_config", models.JSONField(null=True)),
                (
                    "assistant_status",
                    models.CharField(
                        choices=[("drafted", "Drafted"), ("published", "Published")],
                        default="drafted",
                        max_length=10,
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=genflow.apps.assistant.models.get_assistant_media_path,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.entitygroup"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "related_model",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.providermodelconfig",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="team.team",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
