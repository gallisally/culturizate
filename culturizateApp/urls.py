from django.urls import path
from . import views
from .views import CustomLoginView


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
    path('obtener_pregunta_n1',views.obtener_pregunta_n1,name='obtener_pregunta_n1'),
]


