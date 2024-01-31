from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from bootstrap5.widgets import RadioSelectButtonGroup

class CustomAuthenticationForm(AuthenticationForm):
    # Personaliza el formulario si es necesario
    pass

class MyForm(forms.Form):
    media_type = forms.ChoiceField(
        help_text="Select the order type.",
        required=True,
        label="Order Type:",
        widget=RadioSelectButtonGroup,
        choices=((1, 'Vinyl'), (2, 'Compact Disc')),
        initial=1,
    )



class SignIn(UserCreationForm):
    name = forms.CharField(label="Your name", max_length=100)
    surname_1=forms.CharField(label=' Primer apellido', max_length=100)
    surname_2=forms.CharField(label=' Segundo apellido', max_length=100)
    password=forms.CharField(label=' Contraseña', max_length=100)

    class Meta:
        model = UserProfile
        fields = ('username', 'name', 'surname_1', 'surname_2', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.surname_1 = self.cleaned_data['surname_1']
        user.surname_1 = self.cleaned_data['surname_2']
        if commit:
            user.save()
        return user

