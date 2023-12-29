from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomAuthenticationForm(AuthenticationForm):
    # Personaliza el formulario si es necesario
    pass
class UserForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    email = forms.EmailField()
    password = forms.CharField(max_length=255)

class UserProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ('name', 'surname', 'email')

class UserAnswerForm(forms.Form):
    #campo user_name para recoger respuesta de usuario inicializando lista choices vacia utilizando botones de readio
    user_answer=forms.ChoiceField(choices=['A','B','C'],widget=forms.RadioSelect)
    #metodo que se inicializa cuando se crea instancia del formulario
    def __init__(self,*args,**kwargs):
        #se extrae argumentos choices del dicc kwarks. sino existe en kwargs lista choices vacia
        choices=kwargs.pop('choices',[])
        #llama a init para realizar cualquier iniciallizacion necesaria
        super(UserAnswerForm, self).__init__(*args, **kwargs)
        #Configura las opciones del campo 'user_answer' utilizando el valor extraído
        #del diccionario de argumentos de palabra clave. Esto permite dinámicamente establecer las opciones del campo durante la inicialización del formulario.
        self.fields['user_answer'].choices = [(option, option) for option in choices]
       