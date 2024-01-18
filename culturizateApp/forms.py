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

