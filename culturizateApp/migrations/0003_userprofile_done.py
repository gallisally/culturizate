# Generated by Django 4.2.9 on 2024-01-29 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("culturizateApp", "0002_userprofile_correct_answers_userprofile_fails"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="done",
            field=models.IntegerField(default=0),
        ),
    ]