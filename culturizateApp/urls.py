from django.urls import path
from . import views
from .views import CustomLoginView
from .views import game
from .views import obtain_categories



"""
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("signin/",views.signin_view,name='signin'),
   # path('login-with-template/', CustomLoginViewWithTemplate.as_view(), name='login_with_template'),
    path('accounts/profile/',views.user_profile,name='profile'),
    path('game/',views.obtener_pregunta_n1,name='game'),
    #path('logout/', CustomLogoutView.as_view(), name='logout'),
]
"""
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("signin/", views.signin_view, name='signin'),
    # path('login-with-template/', CustomLoginViewWithTemplate.as_view(), name='login_with_template'),
    path('accounts/profile/', views.user_profile, name='profile'),
    path('game/',views.game,name='game'),
    path('obtener_pregunta_n1/<str:category_selected>/',views.obtener_pregunta_n1,name='obtener_pregunta_n1'),
    #path('obtener_pregunta_n1/(?P<category_selected>[^/]+)/\\Z',views.obtener_pregunta_n1, name='obtener_pregunta_n1'),
    path('checkAnswer/',views.checkAnswer,name='checkAnswer'),
    path('obtain_categories/',views.obtain_categories,name='obtain_categories'),
]


