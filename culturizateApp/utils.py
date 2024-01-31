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
from .models import Cuadro,UserProfile
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
        questions_set=random.sample(list(society_questions),11)
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
        self.user_profile.sociedad_actual_score=0
        i=1
        self.user_profile.sociedad_test_score=self.user_profile.sociedad_last_score
        self.user_profile.save()
        #user_profile=request.user
        try:
            if self.request.method == 'GET':  
                question_set_dicts=self.get_random_question()
                remaining_questions=question_set_dicts.copy()
                question = remaining_questions.pop(0)
                
                if question is not None:
                    options = [
                        ('A', question['option_a']),
                        ('B', question['option_b']),
                        ('C', question['option_c']),
                    ]
                    opt_cor = options[0][1] 
                    opt_cor_letter=options[0][0]
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
                        'i':i,
                        'opt_cor':opt_cor,
                        'opt_cor_letter':opt_cor_letter,
                       
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
                        'current_question': self.current_question,
                        'i':i,
                         
                    }
                    self.request.session['i'] = i


                    #self.request.session['current_question'] = self.current_question
                    self.request.session['opt_cor']=opt_cor
                    self.request.session['opt_cor_letter']=opt_cor_letter

                    self.request.session['remaining_questions'] = remaining_questions
                    #self.current.session['current_question']=context
                    return context
                return HttpResponse('Esta vista solo admite solicitudes GET')
        except Exception as e:
            logging.exception(e)
            print(f"Error: {type(e).__name__} - {str(e)}")
            return HttpResponse('Error, vuelve a intentarlo más tarde')
  
    def next_cultural_question(self):
        remaining_questions = self.request.session.get('remaining_questions')
        i=self.request.session.get('i')
        #self.current_question=self.request.session.get('current_question')
        #print(f"remaining_questions antes de pop: {remaining_questions}")
        if remaining_questions and len(remaining_questions) > 1:
            i+=1
            question = remaining_questions.pop(0)
            if question is not None:
                remaining_questions = remaining_questions.copy()
                options = [
                        ('A', question['option_a']),
                        ('B', question['option_b']),
                        ('C', question['option_c']),
                ]
                opt_cor = options[0][1]
                opt_cor_letter=options[0][0] 
                self.user_profile.round += 1
                self.user_profile.save()
                options = sorted(options, key=lambda x: choice([0, 1, 2]))
                current_question = {
                    'question_text' : question['question_text'],
                    'options':options,
                    'points':question['points'],
                    'nivel_dificultad':question['nivel_dificultad'],
                    'category':question['category'],
                    'correct_answer':question['correct_option'],
                    'round':self.user_profile.round,
                    'i':i,
                    'opt_cor':opt_cor,
                    'opt_cor_letter':opt_cor_letter,   
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
                    'i':i,
                    'current_question':self.current_question,
                    'sociedad_actual_score':self.user_profile.sociedad_actual_score, 
                    'opt_cor':opt_cor,   
                }
              
                self.request.session['opt_cor_letter']=opt_cor_letter
                self.request.session['sociedad_actual_score']=self.user_profile.sociedad_actual_score
                self.request.session['current_question'] = current_question
                self.request.session['i']=i
                self.request.session['opt_cor']=opt_cor
                # Almacena las preguntas restantes en la sesión
                self.request.session['remaining_questions'] = remaining_questions
                return context
        else:
           
            print('No hay mas oreguntas')
            response_result_message = None

            if self.user_profile.sociedad_actual_score > self.user_profile.sociedad_test_score:
                print(f'tu puntuacion ha mejorado')
                #self.current_question['response_message']='Enhorabuena! Tus resultados han mejorado'
                self.user_profile.sociedad_test_message='Enhorabuena! Tus resultados han mejorado'
            elif self.user_profile.sociedad_actual_score < self.user_profile.sociedad_test_score:
                print('tus resultaos han empeorado')
                self.user_profile.sociedad_test_message='Tu puntuacion ha empeorado. Culturizate'
                #self.current_question['response_message']='Tus resultados han empeorado, culturizate'
            elif self.user_profile.sociedad_actual_score==self.user_profile.sociedad_test_score:
                self.user_profile.sociedad_test_message='Tu puntuacion sigue igual que la anterior'
            
            context={
                'current_question': self.current_question,
                'response_result_message':response_result_message,
            }   

          
            self.user_profile.sociedad_last_score=self.user_profile.sociedad_actual_score
            self.user_profile.save() 
            print(f'actual_score: {self.user_profile.sociedad_actual_score}')  
            print(f'last score: {self.user_profile.sociedad_last_score}')  
            print(f'test score: {self.user_profile.sociedad_test_score}')             
            #self.request.session['current_question'] = self.current_question
            self.request.session['response_result_message'] =response_result_message
            print(f'puntuacion registrada {self.user_profile.sociedad_test_score}')
            print(f'puntuacion reiniciada {self.user_profile.sociedad_actual_score}')
            return context

    def checkCulturalAnswer(self,user_answer):
        self.current_question=self.request.session.get('current_question')
        opt_cor = self.request.session.get('opt_cor')
        opt_cor_letter = self.request.session.get('opt_cor_letter')

        if self.current_question:
            self.user_profile.done+=1
            self.user_profile.save()
            if user_answer== opt_cor_letter:
                print('bien')
                response_message='has acertado!'
                self.user_profile.sociedad_actual_score+=10
                self.user_profile.save()
            else:
                self.user_profile.fails+=1
                self.user_profile.save()
                print('mal')
                response_message=(f'Has fallado!, la respuesta correcta es: {opt_cor}')
                self.user_profile.save()
            context = {
                'question_text': self.current_question['question_text'],
                'options': self.current_question['options'],
                'points': self.current_question['points'],
                'nivel_dificultad': self.current_question['nivel_dificultad'],
                'category': self.current_question['category'],
                'correct_answer': self.current_question['correct_answer'],
                'round': self.user_profile.round,
                'sociedad_actual_score':self.user_profile.sociedad_actual_score,
                'response_message': response_message,
            }
            
            self.current_question['sociedad_actual_score']=self.user_profile.sociedad_actual_score
            self.current_question['response_message'] = response_message
            self.request.session['response_message'] = response_message
            return context       
        else:
            print('nada omnada')
            return {'message': 'No se ha podido verificar la pregunta'}



class ArtTest:
    def __init__(self, request):
        self.request = request
        self.user_profile = request.user
        self.current_question = {}

    def get_random_question(self):
        #society_questions=BaseQuestion.objects.filter(category='sociedad')
        art_questions=Cuadro.objects.order_by('?')
        questions_set=random.sample(list(art_questions),10)
        questions_set_dicts = [
            {
                'cuadro': question.cuadro,
                'autor': question.autor,
                'year': question.year,
                'description':question.description,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'image':question.image,

            }
            for question in questions_set
        ]
        return questions_set_dicts


    def start_art_test(self,request):
        self.user_profile.art_actual_score=0
        i=1
        self.user_profile.art_test_score=self.user_profile.art_last_score
        self.user_profile.save()
        #user_profile=request.user
        try:
            if self.request.method == 'GET':  
                question_set_dicts=self.get_random_question()
                remaining_questions=question_set_dicts.copy()
                question = remaining_questions.pop(0)
                
                if question is not None:
                    options = [
                        ('A', question['option_a']),
                        ('B', question['option_b']),
                        ('C', question['option_c']),
                    ]
                    opt_cor = options[0][1] 
                    opt_cor_letter=options[0][0]
                    self.user_profile.round += 1
                    self.user_profile.save()
                    options = sorted(options, key=lambda x: choice([0, 1, 2]))
                    self.current_question = {
                       
                        'cuadro': question['cuadro'],
                        'autor': question['autor'],
                        'year': question['year'],
                        'description':question['description'],
                        'option_a': question['option_a'],
                        'option_b': question['option_b'],
                        'option_c': question['option_c'],
                        'image':question['image'],
                        'i':i,
                        'options': options,
                        'opt_cor':opt_cor,
                        'opt_cor_letter':opt_cor_letter,
                            
                    }


                    context = {
                        'cuadro': question['cuadro'],
                        'autor': question['autor'],
                        'year': question['year'],
                        'description':question['description'],
                        'option_a': question['option_a'],
                        'option_b': question['option_b'],
                        'option_c': question['option_c'],
                        'image':question['image'],
                        'remaining_questions':remaining_questions,
                        'current_question': self.current_question,
                        'i':i,    
                        'options':options, 
                    }
                    self.request.session['i'] = i
                    self.request.session['opt_cor']=opt_cor
                    self.request.session['options']=options
                    self.request.session['opt_cor_letter']=opt_cor_letter
                    self.request.session['remaining_questions'] = remaining_questions
                    print(f'optins: {options}')
                    return context
                return HttpResponse('Esta vista solo admite solicitudes GET')
        except Exception as e:
            logging.exception(e)
            print(f"Error: {type(e).__name__} - {str(e)}")
            return HttpResponse('Error, vuelve a intentarlo más tarde')
  
    def next_art_question(self):
        remaining_questions = self.request.session.get('remaining_questions')

        i=self.request.session.get('i')
        if remaining_questions and len(remaining_questions) > 1:
            i+=1
            question = remaining_questions.pop(0)
            if question is not None:
                remaining_questions = remaining_questions.copy()
                options = [
                        ('A', question['option_a']),
                        ('B', question['option_b']),
                        ('C', question['option_c']),
                ]
                opt_cor = options[0][1]
                opt_cor_letter=options[0][0] 
                self.user_profile.round += 1
                self.user_profile.save()
                options = sorted(options, key=lambda x: choice([0, 1, 2]))
                current_question = {

                    'cuadro': question['cuadro'],
                    'autor': question['autor'],
                    'year': question['year'],
                    'description':question['description'],
                    'option_a': question['option_a'],
                    'option_b': question['option_b'],
                    'option_c': question['option_c'],
                    'image':question['image'],
                    'remaining_questions':remaining_questions,
                    'current_question': self.current_question,
                    'i':i,    
                    'options':options, 
                    'opt_cor':opt_cor,
                    'opt_cor_letter':opt_cor_letter,   
                } 
                context = {

                    'cuadro': question['cuadro'],
                    'autor': question['autor'],
                    'year': question['year'],
                    'description':question['description'],
                    'option_a': question['option_a'],
                    'option_b': question['option_b'],
                    'option_c': question['option_c'],
                    'image':question['image'],
                    'remaining_questions':remaining_questions,
                    'current_question': self.current_question,
                    'i':i,    
                    'options':options, 
                    'opt_cor':opt_cor,
                    'opt_cor_letter':opt_cor_letter, 
                    'art_actual_score':self.user_profile.sociedad_actual_score, 
  
                }
                self.request.session['remaining_questions'] = remaining_questions.copy()

                self.request.session['opt_cor_letter']=opt_cor_letter
                self.request.session['art_actual_score']=self.user_profile.art_actual_score
                self.request.session['current_question'] = current_question
                self.request.session['i']=i
                self.request.session['opt_cor']=opt_cor
                # Almacena las preguntas restantes en la sesión
                self.request.session['remaining_questions'] = remaining_questions
                return context
        else:
           
            print('No hay mas oreguntas')
            response_result_message = None
            self.request.session['remaining_questions'] = remaining_questions


            if self.user_profile.art_actual_score > self.user_profile.art_test_score:
                print(f'actual_score: {self.user_profile.art_actual_score}, test_score: {self.user_profile.art_test_score}')
                print(f'tu puntuacion ha mejorado')
                #self.current_question['response_message']='Enhorabuena! Tus resultados han mejorado'
                self.user_profile.art_test_message='Enhorabuena! Tus resultados han mejorado'
            elif self.user_profile.art_actual_score < self.user_profile.art_test_score:
                print(f'actual_score: {self.user_profile.art_actual_score}, test_score: {self.user_profile.art_test_score}')

                print('tus resultaos han empeorado')
                self.user_profile.art_test_message='Tu puntuacion ha empeorado. Culturizate'
                #self.current_question['response_message']='Tus resultados han empeorado, culturizate'
            elif self.user_profile.art_actual_score==self.user_profile.art_test_score:
                print(f'actual_score: {self.user_profile.art_actual_score}, test_score: {self.user_profile.art_test_score}')

                self.user_profile.art_test_message='Tu puntuacion sigue igual que la anterior'
            
            context={
                'current_question': self.current_question,
                'response_result_message':response_result_message,
            }   
            self.user_profile.art_last_score=self.user_profile.art_actual_score
            self.user_profile.save() 
            print(f'actual_score: {self.user_profile.art_actual_score}')  
            print(f'last score: {self.user_profile.art_last_score}')  
            print(f'test score: {self.user_profile.art_test_score}')             
            #self.request.session['current_question'] = self.current_question
            self.request.session['response_result_message'] =response_result_message
            print(f'puntuacion registrada test {self.user_profile.art_test_score}')
            print(f'puntuacion reiniciada {self.user_profile.art_actual_score}')

            print(f'puntuacion registrada test {self.user_profile.art_test_score}')

            return context
         

    def checkArtAnswer(self,user_answer):
        self.current_question=self.request.session.get('current_question')
        opt_cor = self.request.session.get('opt_cor')
        opt_cor_letter = self.request.session.get('opt_cor_letter')

        if self.current_question:
            self.user_profile.done+=1
            self.user_profile.save()

            if user_answer== opt_cor_letter:
                print('bien')
                response_message='has acertado!'
                self.user_profile.art_actual_score+=10
                self.user_profile.correct_answers+=1
                self.user_profile.save()

            else:
                print('mal')
                response_message=(f'Has fallado!, la respuesta correcta es: {opt_cor}')
                self.user_profile.fails+=1
                self.user_profile.save()
            context = {
                'cuadro': self.current_question['cuadro'],
                'autor': self.current_question['autor'],
                'year': self.current_question['year'],
                'description':self.current_question['description'],
                'image':self.current_question['image'],
                #'current_question': self.current_question,
                #'opt_cor':opt_cor,
                #'opt_cor_letter':opt_cor_letter, 
                'art_actual_score':self.user_profile.sociedad_actual_score, 
                'options': self.current_question['options'],
                'sociedad_actual_score':self.user_profile.sociedad_actual_score,
                'response_message': response_message,
            }
            
            self.current_question['art_actual_score']=self.user_profile.sociedad_actual_score
            self.current_question['response_message'] = response_message
            self.request.session['response_message'] = response_message
            return context       
        else:
            print('nada omnada')
            return {'message': 'No se ha podido verificar la pregunta'}
    
    
    
class UserResults:
    def __init__(self,request):
        self.request=request
        #self.user_profile=self.user
        #self.user_profile = UserProfile.objects.all()
        self.users=UserProfile.objects.all()



    def fails_avg(self):
        fails_avg_dict=[]
        for user in self.users:
            if user.done==0:
                print(f'usuario  {user}')
                print(f'Aun no has realizado ningun test: {user.done}')
                fails_avg=0
                fails_avg_dict.append({'username':user.name,'fails_avg':fails_avg})


            else:
                print(f' {user},fails:{user.fails}, done:{user.done}')

                fails_avg=((user.fails/user.done) * 100)
                #user.save()
                fails_avg_dict.append({'username':user.name,'fails_avg':fails_avg})
        return fails_avg_dict
    
    def art_results(self):
        art_results_dict=[]
        for user in self.users:
            print(f'usuario  {user}')
            art_last_score=user.art_last_score
            print(f' {user},las_score:{user.art_last_score}')
            #user.save()
            art_results_dict.append({'username':user.name,'art_last_score':art_last_score})
            print(f'diccionario en utils: {art_results_dict}')
        return art_results_dict
    
    def cultural_results(self):
        cultural_results_dict=[]
        for user in self.users:
            print(f'usuario  {user}')
            sociedad_last_score=user.sociedad_last_score
            print(f' {user},las_score:{user.sociedad_last_score}')
            #user.save()
            cultural_results_dict.append({'username':user.name,'cultural_last_score':sociedad_last_score})
            print(f'diccionario en utils: {cultural_results_dict}')
        return cultural_results_dict

