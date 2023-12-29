from django.db import models
import random
from .models import BaseQuestion
from random import choice
from django.http import HttpResponse
from django.shortcuts import render

class User:
    def __init__(self,username):
        self.username=username
        self.score=0
        self.attempts=0

    def increase_score(self,points):
        self.score += points
    
    def incorrect_attempts(self,attempt):
        self.attempts +=1
class Question:
    def __init__(self, question_text,correct_option,options,answer):
        self.question_text=question_text
        self.correct_option=correct_option
        self.options=options

    def is_correct(self,user_answer,correct_option):
        return user_answer==correct_option
class GameManager:
    def __init__(self,questions):
        self.questions=questions
        self.current_question=None
        self.users={}

    def add_user(self,username):
        if username not in self.users:
            self.users[username]=User[username]

    def random_question(self):
        self.current_question=random.choice(self.questions)

    def handle_answer(self,user_answer,username):
        user=self.users.get(username)
        if user and self.current_question:
            if self.current_question.is_correct(user_answer):
                user.increase_score(10)
            else:
                user.increase.attempts()

    def get_user_score(self,username):
        user=self.user.get(username)
        return user.score if user else None
    
"""
questions = [Question(**data) for data in questions_data]
game_manager = GameManager(questions)

# Agregar usuarios
game_manager.add_user("Usuario1")
game_manager.add_user("Usuario2")

# Jugar una ronda
game_manager.select_random_question()
game_manager.handle_answer("Usuario1", "B")
game_manager.handle_answer("Usuario2", "A")

# Obtener puntuaciones
score_user1 = game_manager.get_user_score("Usuario1")
score_user2 = game_manager.get_user_score("Usuario2")

print(f"Puntuación de Usuario1: {score_user1}")
print(f"Puntuación de Usuario2: {score_user2}")

"""

def obtener_pregunta_n1(request=None):
    question=BaseQuestion.objects.filter(nivel_dificultad=1).order_by('?').first()
    if question is not None:
        options=[
            ('A',question.option_a),
            ('B',question.option_b),
            ('C',question.option_c),
        ]
        options=sorted(options,key=lambda x:choice([0,1,2]))
        context = {
            'question_text' : question.question_text,
            'options':options,
            'points':question.points,
            'category':question.category,
            'coorect_answer':question.correct_option
            }

        return render(request,'game.html',context)
    else:
       return HttpResponse('No ha preguntas que correspondan a ese nivel de dificultad')
