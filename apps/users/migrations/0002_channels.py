# Generated by Django 4.2.4 on 2024-05-19 12:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Channels",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "username",
                    models.CharField(
                        help_text=" @'siz (Misol: alisher_sadullaev)",
                        max_length=123,
                        verbose_name="username",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "channel",
                "verbose_name_plural": "channels",
                "ordering": ["order"],
            },
        ),
    ]
