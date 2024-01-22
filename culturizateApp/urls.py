from django.urls import path
from . import views
from .views import CustomLoginView
from .views import game
from .views import obtain_categories




urlpatterns = [
    path("", views.index, name="index"),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("signin/", views.signin_view, name='signin'),
    path("perfil/",views.perfil,name='perfil'),
    # path('login-with-template/', CustomLoginViewWithTemplate.as_view(), name='login_with_template'),
    path('accounts/profile/', views.user_profile, name='profile'),
    #path('entrenate/',views.entrenate,name='entrenate'),
    path('game/',views.game,name='game'),
    path("take_question/<str:category_selected>/<int:nivel>/",views.take_question,name='take_question'),
    #path('obtener_pregunta_n1/(?P<category_selected>[^/]+)/\\Z',views.obtener_pregunta_n1, name='obtener_pregunta_n1'),
    path('checkAnswer/',views.checkAnswer,name='checkAnswer'),
    path('obtain_categories/',views.obtain_categories,name='obtain_categories'),
    path('play/',views.play,name="play"),
    path('get_tested/',views.get_tested,name='get_tested'),
    path('art_test/',views.art_test,name='art_test'),
    path('art_question/',views.art_question,name='art_question'),
    path('checkArtAnswer/',views.checkArtAnswer,name='checkArtAnswer'),
    path('society_question_test/',views.society_question_test,name='society_question_test'),
    path('next_question_view/',views.next_question_view,name='next_question_view')
]


