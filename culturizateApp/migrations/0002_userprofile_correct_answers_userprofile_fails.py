# Generated by Django 4.2.9 on 2024-01-29 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("culturizateApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="correct_answers",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="fails",
            field=models.IntegerField(default=0),
        ),
    ]
