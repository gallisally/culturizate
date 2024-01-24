from django.db import models
from django.contrib.auth.models import AbstractUser
"""
class User(AbstractUser):
    score=models.IntegerField(default=0)
"""



class UserProfile(AbstractUser):
    name = models.CharField(max_length=255)
    surname=models.CharField(max_length=200)
    #age=models.IntegerField(null=False, blank=False)
    email = models.EmailField()
    score = models.IntegerField(default=0)
    art_score=models.IntegerField(default=0)
    iq_score=models.IntegerField(default=0)
    culture_score=models.IntegerField(default=0)

    attempts = models.IntegerField(default=0)
    informatica_score=models.IntegerField(default=0)
    ciencia_score=models.IntegerField(default=0)
    historia_score=models.IntegerField(default=0)
    geopolitica_score=models.IntegerField(default=0)
    curiosidades_score=models.IntegerField(default=0)
    espiritualidad_score=models.IntegerField(default=0)
    historia_score=models.IntegerField(default=0)

    sociedad_points=models.IntegerField(default=0)
    sociedad_actual_score=models.IntegerField(default=0)
    #SIN USAR
    sociedad_last_score=models.IntegerField(default=0)
    sociedad_test_score=models.IntegerField(default=0)
    sociedad_test_message=models.CharField(max_length=100)
    
    art_attempts=models.IntegerField(default=2)
    iq_attempts=models.IntegerField(default=2)
    culture_attempts=models.IntegerField(default=2)

    art_success=models.IntegerField(default=0)
    art_errors=models.IntegerField(default=0)
    round=models.IntegerField(default=0)
    art_test_score=models.IntegerField(default=0)
    initial_score=models.IntegerField(default=0)
    









class BaseQuestion(models.Model):
    question_text = models.TextField()
    correct_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C')])
    nivel_dificultad = models.IntegerField()
    category = models.CharField(max_length=200)
    points=models.IntegerField()
    option_a = models.CharField(max_length=255,null=True)
    option_b = models.CharField(max_length=255,null=True)
    option_c = models.CharField(max_length=255,null=True)
    

class Puntuacion(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(BaseQuestion, on_delete=models.CASCADE)
    puntos=models.IntegerField()
    #respuesta = models.CharField(max_length=255)
    #correcta = models.BooleanField()


class Cuadro(models.Model):
    cuadro=models.CharField(max_length=500)
    autor=models.CharField(max_length=200)
    year=models.CharField(max_length=10)
    description=models.CharField(max_length=10000)
    a=models.CharField(max_length=200)
    b=models.CharField(max_length=200)
    c=models.CharField(max_length=200)
    image=models.CharField(max_length=400)




    