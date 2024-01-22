from django.db import models
import random
from .models import BaseQuestion
from random import choice
from django.http import HttpResponse
from django.shortcuts import render

import random
from django.db.models import Count
    
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cuadro
import logging
from random import choice
import json

class CulturalTest:
    def __init__(self, request):
        self.request = request
        self.user_profile = request.user
        self.current_question = {}

    def get_random_question(self):
        society_questions=BaseQuestion.objects.filter(category='sociedad')
        questions_set=random.sample(list(society_questions),10)
        questions_set_dicts = [
            {
                'question_text': question.question_text,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'correct_option': question.correct_option,
                'nivel_dificultad': question.nivel_dificultad,
                'category': question.category,
                'points': question.points,
            }
            for question in questions_set
        ]

        return questions_set_dicts


    def start_cultural_test(self,request):
        user_profile=request.user
        try:
            if self.request.method == 'GET':  
                question_set_dicts=self.get_random_question()
                remaining_questions=question_set_dicts.copy()
                question = question_set_dicts.pop(0)
                
                if question is not None:
                    options = [
                        ('A', question['option_a']),
                        ('B', question['option_b']),
                        ('C', question['option_c']),
                    ]
                    self.user_profile.round += 1
                    self.user_profile.save()
                    options = sorted(options, key=lambda x: choice([0, 1, 2]))
                    self.current_question = {
                        'question_text' : question['question_text'],
                        'options':options,
                        'points':question['points'],
                        'nivel_dificultad':question['nivel_dificultad'],
                        'category':question['category'],
                        'correct_answer':question['correct_option'],
                        'round':self.user_profile.round,
                    }

                    context = {
                        'question_text':question['question_text'],
                        'options': options,
                        'points': question['points'],
                        'nivel_dificultad': question['nivel_dificultad'],
                        'category': question['category'],
                        'correct_answer': question['correct_option'],
                        'round':self.user_profile.round,
                        'remaining_questions':remaining_questions,
                        
                    }
                    self.request.session['remaining_questions'] = remaining_questions

                    #print(f'contexto= {context}')
                    #return render(self.request, 'society_test.html', context)
                    return context
                return HttpResponse('Esta vista solo admite solicitudes GET')
        except Exception as e:
            logging.exception(e)
            print(f"Error: {type(e).__name__} - {str(e)}")
            return HttpResponse('Error, vuelve a intentarlo más tarde')
  
    def next_cultural_question(self):
        remaining_questions = self.request.session.get('remaining_questions')
        print(f"remaining_questions antes de pop: {remaining_questions}")

        if remaining_questions:
            question = remaining_questions.pop(0)
            if question is not None:
                remaining_questions = remaining_questions.copy()

                options = [
                        ('A', question['option_a']),
                        ('B', question['option_b']),
                    ('C', question['option_c']),
                ]
                self.user_profile.round += 1
                self.user_profile.save()
                options = sorted(options, key=lambda x: choice([0, 1, 2]))
                self.current_question = {
                    'question_text' : question['question_text'],
                    'options':options,
                    'points':question['points'],
                    'nivel_dificultad':question['nivel_dificultad'],
                    'category':question['category'],
                    'correct_answer':question['correct_option'],
                    'round':self.user_profile.round,
                }

                context = {
                    'question_text':question['question_text'],
                    'options': options,
                    'points': question['points'],
                    'nivel_dificultad': question['nivel_dificultad'],
                    'category': question['category'],
                    'correct_answer': question['correct_option'],
                    'round':self.user_profile.round,
                    'remaining_questions': remaining_questions,
                    
                }
                # Almacena las preguntas restantes en la sesión
                self.request.session['remaining_questions'] = remaining_questions

                
                return context
        else:
            return {'message': 'No hay más preguntas.'}

        
    def end_art_test(self):
        self.current_question = self.request.session.get('current_question', {})
        self.user_profile.round = 0

        if self.user_profile.initial_score > self.user_profile.art_test_score:
            print(f'Tu resultado ha mejorado el de antes es de {self.user_profile.art_test_score}|n el de ahora es {self.user_profile.initial_score}')
            new_art_score_message = 'Nuevo record registrado!'
        elif self.user_profile.initial_score == self.user_profile.art_test_score:
            print(f'Tu resultado es igual el de antes es de {self.user_profile.art_test_score}|n el de ahora es {self.user_profile.initial_score}')
            new_art_score_message = 'Tu nota sigue igual'
        else:
            print(f'Tu resultado ha empeorado el de antes es de {self.user_profile.art_test_score}|n el de ahora es {self.user_profile.initial_score}')
            new_art_score_message = 'Tu resultado del test ha empeorado, estudia más.'

        self.user_profile.art_test_score = self.user_profile.initial_score
        self.user_profile.initial_score = 0

        print('El test ha acabado')
        self.current_question['new_art_score_message'] = new_art_score_message
        self.user_profile.save()

    @staticmethod
    def check_art_answer(request):
        if request.method == 'POST':
            user_answer = request.POST.get('user_answer')
            current_question = request.session.get('current_question', {})
            user_profile = request.user
            response_message = ''

            if user_answer == 'a':
                response_message = 'Has acertado!'
                user_profile.initial_score += 10
                user_profile.art_success += 1
                print(f'Respuesta correcta, tu puntuación es de {user_profile.art_score}')
            else:
                response_message = 'Has fallado!. Prueba una vez más'
                user_profile.art_errors += 1

            user_profile.save()
            current_question['response_message'] = response_message
            current_question['art_success'] = user_profile.art_success
            current_question['initial_score'] = user_profile.initial_score
            current_question['art_errors'] = user_profile.art_errors
            request.session['current_question'] = current_question

            return JsonResponse(current_question)

        return HttpResponse('La función checkAnswer solo admite solicitudes POST')

# Uso en tus vistas