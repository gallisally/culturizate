from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.contrib.auth.views import LoginView,LogoutView
from .forms import CustomAuthenticationForm
from django.views.generic.edit import FormView
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import BaseQuestion,UserProfile
from .forms import UserAnswerForm
from random import choice
from .utils import obtener_pregunta_n1





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

@login_required
def user_profile(request):
    user=request.user
    return render(request,'user_profile.html',{'user':user})

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
"""
def questions_l1(request):
    question = obtener_pregunta_n1()
    if isinstance(question,dict):
        context={'question':question}
        return render(request,'game.html',context)
    else:
        #si no hay diccionario devuelve directamente respuesta http
        return question

"""

def obtener_pregunta_n1(request):
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
            'nivel_dificultad':question.nivel_dificultad,
            'category':question.category,
            'correct_answer':question.correct_option
            }

        return render(request,'game.html',context)
    else:
       return HttpResponse('No ha preguntas que correspondan a ese nivel de dificultad')

    

"""
class CustomLoginViewWithTemplate(FormView):
    template_name = 'login.html'  # Ruta relativa a la carpeta 'templates'
    form_class = CustomAuthenticationForm
    success_url = '/'  # Ajusta la URL de redirección después del inicio de sesión

    def form_valid(self, form):
        # Lógica adicional después de un inicio de sesión exitoso
        return super().form_valid(form)

    def form_invalid(self, form):
        # Lógica adicional en caso de formulario no válido
        return super().form_invalid(form)
    

 
class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        required=True
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Iniciar Sesión'))



def handle_answer(request, question_id, selected_option):
    try:
        question = MultipleChoiceQuestion.objects.get(pk=question_id)
    except MultipleChoiceQuestion.DoesNotExist:
        try:
            question = TrueFalseQuestion.objects.get(pk=question_id)
        except TrueFalseQuestion.DoesNotExist:
            # Manejar el caso en el que la pregunta no existe
            return HttpResponse("La pregunta no existe")

    # Resto del código para manejar la respuesta y renderizar la próxima pregunta, por ejemplo.

    return render(request, 'next_question_template.html', context)
"""

"""
def play_game(request):
    def play_game(request):
    # Se asume que ya has configurado tus preguntas en alguna parte
        questions_data = [
            {"text": "¿Cuál es la capital de Francia?", "options": ["A) Madrid", "B) París", "C) Londres"], "correct_option": "B"},
            {"text": "¿Cuál es el resultado de 2 + 2?", "options": ["A) 3", "B) 4", "C) 5"], "correct_option": "B"},
            # ... otras preguntas ...
        ]

        questions = [Question(**data) for data in questions_data]
        game_manager = GameManager(questions)

        # Obtenemos el nombre de usuario del request (puedes ajustar esto según tu autenticación)
        username = request.user.username if request.user.is_authenticated else 'Anónimo'

        # Añadimos al usuario al juego
        game_manager.add_user(username)

        # Seleccionamos una pregunta al azar para empezar
        game_manager.select_random_question()

        # Lógica para manejar la respuesta del usuario (esto puede ser más complejo dependiendo de tu aplicación)
        if request.method == 'POST':
            user_answer = request.POST.get('user_answer')  # Suponiendo que has enviado la respuesta del usuario mediante un formulario
            game_manager.handle_answer(username, user_answer)

        # Obtenemos la puntuación actual del usuario
        user_score = game_manager.get_user_score(username)

        # Preparamos el contexto para la plantilla
        context = {
            'current_question': game_manager.current_question,
            'user_score': user_score,
        }

        return render(request, 'game/play_game.html', context)

"""
