from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.contrib.auth.views import LoginView,LogoutView
from .forms import CustomAuthenticationForm
from django.views.generic.edit import FormView
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
#from .forms import UserProfileCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import BaseQuestion,UserProfile,Cuadro
#from .forms import UserAnswerForm
from random import choice
import logging
from django.views.generic import View
from .forms import MyForm
from django.http import JsonResponse
from .utils import CulturalTest






#from utils import GameManager


"""
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
"""

def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def signin_view(request):
    form = UserProfileCreationForm()

    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a donde desees después de un registro exitoso
            return redirect('login')

    context = {'form': form}
    return render(request, 'signin.html', context)
"""
@login_required
def user_profile(request):
    user=request.user
    all_categories = ["informatica", "historia", "geopolitica", "espiritualidad", "curiosidades", "ciencia"]

    return render(request,'user_profile.html',{'user':user,'all_categories': all_categories})

"""


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = MyForm()
    return render(request, 'user_profile.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'  # Ajusta la plantilla según tus necesidades
    success_url=reverse_lazy('game')



def play_game(request):
    questions=BaseQuestion.objects.filter(nivel_dificultad=1).order_by('?')[:10]

    if request.method=='POST':
        #procesar respuesta usuario
        #form=UserAnswerForm(request.POST)
        #form = UserAnswerForm(request.POST, choices=['A', 'B', 'C'])
        form = UserAnswerForm(request.POST, choices=[option.correct_option for option in questions])

        if form.is_valid():
            user_answer=form.cleaned_data['user_answer']
            correct_answer=questions[form.cleaned_data['question_index']]
            if user_answer == correct_answer:
                user_profile=UserProfile.get.object(user=request.user)
                user_profile.score +=questions[form.cleaned_data['question_index']].points
                user_profile.save()
            return redirect('play_game')
        else:
            #form=UserAnswerForm(choices=['A','B','C'])
            form = UserAnswerForm(choices=[option.correct_option for option in questions])
            context={
                'question':questions,
                'form':form
            }
            return render(request, 'game.html', context)
    else:
        #form = UserAnswerForm()
        #form = UserAnswerForm(choices=['A', 'B', 'C'])
        form = UserAnswerForm(choices=[option.correct_option for option in questions])
        context = {
            'questions': questions,
            'form': form
        }
    return render(request, 'game.html', context)

def game(request):
    return render(request,'game.html')

def perfil(request):
    return render(request,'perfil.html')


def obtain_categories(request):
    all_categories = ["informatica", "historia", "geopolitica", "espiritualidad", "curiosidades", "ciencia"]
    colors=["btn-outline-primary","btn-outline-light","btn-outline-success", "btn-outline-danger","btn-outline-warning","btn-outline-info"]
    category_color_list=zip(all_categories,colors)
    return render(request,'entrenate.html',{'category_color_list': category_color_list})


    
def take_question(request,category_selected=None,nivel=None):
    # Obtener todas las categorías disponibles
    #all_categories = BaseQuestion.objects.values_list('category', flat=True).distinct()
    all_categories=['informatica','historia','geopolitica','espiritualidad','curiosidades','ciencia']
    angle = 360 / len(all_categories)
    user_profile=request.user
    if nivel==5:
        question=BaseQuestion.objects.filter(category=category_selected).order_by('?').first()
    else:
        question=BaseQuestion.objects.filter(category=category_selected,nivel_dificultad=nivel).order_by('?').first()
    try:
        if request.method=='GET':
            if question is not None:
                options=[
                    ('A',question.option_a),
                    ('B',question.option_b),
                    ('C',question.option_c),
                ]
                category_score_field=f'{question.category}_score'
                user_category_score=getattr(user_profile,category_score_field)
                options=sorted(options,key=lambda x:choice([0,1,2]))
                request.session['current_question'] = {       
                    'question_text' : question.question_text,
                    'options':options,
                    'points':question.points,
                    'nivel_dificultad':question.nivel_dificultad,
                    'category':question.category,
                    'correct_answer':question.correct_option ,
                    }
                context = {
                'question_text': question.question_text,
                'options': options,
                'points': question.points,
                'nivel_dificultad': question.nivel_dificultad,
                'category': question.category,
                'correct_answer': question.correct_option,
                'all_categories': all_categories,
                'angle': angle,
                'user_category_score':user_category_score,
                'nivel':nivel,
            }
                return render(request,'game.html',context)
            else:
                return render(request,'/')
        return HttpResponse('Esta vista solo adminte solicitudes post')
    except Exception as e:
        logging.exception(e)
        # Imprimir información detallada sobre la excepción
        print(f"Error: {type(e).__name__} - {str(e)}")
        # Manejar el error de manera adecuada, por ejemplo, redirigir a una página de error
        return HttpResponse('Error, vuelve a intentarlo más tarde')
        
        
@login_required
def checkAnswer(request):
    if request.method=='POST':
        user_answer=request.POST.get('user_answer')
        current_question=request.session.get('current_question',{})
        current_category=current_question.get('category',None)
        current_level=current_question.get('nivel_dificultad',None)
        #user_profile=UserProfile.get.object(user=request.user)
        print(f'user_answer: {user_answer}, correct_answer: {current_question["correct_answer"]}')

        user_profile=request.user
        if user_answer ==  current_question['correct_answer']:
            response_message='Has acertado!'
            user_profile.score +=current_question['points']
            print(f'tu puntuaxion es de {user_profile.score}')
            user_profile.save()
            if current_category:
                print(f' hsa elegido la categoria {current_category}')
                user_category_score=getattr(user_profile,f'{current_category}_score')
                user_category_score+=current_question['points']
                setattr(user_profile,f'{current_category}_score',user_category_score)
                user_profile.save()
        else:
            response_message='Has fallado!'
        current_question['response_message']=response_message   
        current_question['score']=user_profile.score
        current_question['user_category_score']= getattr(user_profile, f'{current_category}_score')
        #actualizando diccionario con el mensaje de respuesta
        request.session['current_question']=current_question

        #return render(request,'game.html',current_question)
        return render(request,'game.html',current_question)
    return HttpResponse('La funcion checkAnswer solo admite solicitudes POST')

@login_required
def play(request):
    return render(request,'play.html')

@login_required
def get_tested(request):
    return render(request,'get_tested.html')

@login_required
def art_test(request):
    return render(request,'art_test.html')

def art_question(request):
    question=Cuadro.objects.order_by('?').first()
    user_profile=request.user
    user_profile.save()
    if user_profile.round <= 9:
        try:
            if request.method=='GET':
                if question is not None:
                    options=[
                        ('a',question.a),
                        ('b',question.b),
                        ('c',question.c),
                    ]
                    user_profile.round+=1
                    user_profile.save()
                    options=sorted(options,key=lambda x:choice([0,1,2]))
                    request.session['current_question'] = {       
                        'cuadro' : question.cuadro,
                        'autor':question.autor,
                        'year':question.year,
                        'description':question.description,
                        'options':options,
                        'image':question.image ,
                        'options':options,
                        'correct_answer':question.autor,
                        'score':user_profile.score,
                        'art_score':user_profile.art_score,
                        'art_success':user_profile.art_success,
                        'art_attempts':user_profile.art_attempts,
                        'round':user_profile.round,
                        'initial_score':user_profile.initial_score,
                        'art_test_score':user_profile.art_test_score,
                        
                        }
                    context = {
                        'cuadro' : question.cuadro,
                        'options':options,
                        'autor':question.autor,
                        'year':question.year,
                        'description':question.description,
                        'options':options,
                        'image':question.image,
                        'correct_answer':question.a,
                        'art_score':user_profile.art_score,
                        'art_success':user_profile.art_success,
                        'art_attempts':user_profile.art_attempts,
                        'score':user_profile.score,
                        'round':user_profile.round,
                        'initial_score':user_profile.initial_score,
                        'art_test_score':user_profile.art_test_score,}
                    return render(request,'art_test.html',context)
            return HttpResponse('Esta vista solo adminte solicitudes post')
        except Exception as e:
            logging.exception(e)
            # Imprimir información detallada sobre la excepción
            print(f"Error: {type(e).__name__} - {str(e)}")
            # Manejar el error de manera adecuada, por ejemplo, redirigir a una página de error
            return HttpResponse('Error, vuelve a intentarlo más tarde')
    else:
        current_question=request.session.get('current_question',{})
        user_profile.round=0
        if user_profile.initial_score > user_profile.art_test_score:
            print(f'Tu resultado ha mejorado elde antes es de  {user_profile.art_test_score}|n el de ahora es {user_profile.initial_score}')

            new_art_score_message='Nuevo record registrado!'
        elif user_profile.initial_score == user_profile.art_test_score:
            print(f'Tu resultado es igual elde antes es de  {user_profile.art_test_score}|n el de ahora es {user_profile.initial_score}')
            new_art_score_message='Tu nota sigue igual'
        else:
            print(f'Tu resultado ha emperodado elde antes es de  {user_profile.art_test_score}|n el de ahora es {user_profile.initial_score}')
            new_art_score_message='Tu resultado del test ha empeorado, estudia mas.'
        user_profile.art_test_score=user_profile.initial_score
        user_profile.initial_score=0
        print('el test ha acabado')
        current_question['new_art_score_message']=new_art_score_message
        user_profile.save()
        return redirect('play.html')
            

@login_required
def checkArtAnswer(request):
    if request.method=='POST':
        user_answer=request.POST.get('user_answer')
        current_question=request.session.get('current_question',{})
        user_profile=request.user
        response_message=''
        if user_answer ==  'a':
            response_message='Has acertado!'
            user_profile.initial_score += 10
            user_profile.art_success +=1
            print(f'Respuesta correcta, tu puntuaxion es de {user_profile.art_score}')   
        else:
            response_message='Has fallado!. Prueba una vez mas'
            user_profile.art_errors +=1   
        user_profile.save()   
        current_question['response_message']=response_message   
        current_question['art_success']=user_profile.art_success
        current_question['initial_score']=user_profile.initial_score
        current_question['art_errors']=user_profile.art_errors
        request.session['current_question']=current_question
        return JsonResponse(current_question)   
    return HttpResponse('La función checkAnswer solo admite solicitudes POST')

def end_art_test(request):
    if request.method=='POST':
        current_question=request.session.get('current_question',{})
        user_profile=request.user
        request.session['current_question']=current_question



@login_required
def society_question_test(request):
    art_test_view = CulturalTest(request)
    context=art_test_view.start_cultural_test(request)
    return render(request,'society_test.html',context)

@login_required
def next_question_view(request):
    cultural_test_view=CulturalTest(request)
    context=cultural_test_view.next_cultural_question()
    return render(request,'society_test.html',context)