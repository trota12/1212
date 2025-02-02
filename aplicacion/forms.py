from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario  # Asegúrate de tener el modelo PerfilUsuario definido


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Dirección de correo electrónico'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), label='', required=False)
    second_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Segundo nombre'}), label='', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido Paterno'}), label='')
    second_last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido Materno'}), label='', required=False)
    rut = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'RUT'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña'}), label='')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'second_name', 'last_name', 'second_last_name', 'rut', 'password1', 'password2']



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True, help_text="El email no puede estar vacío.")
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ['username', 'email', 'password']
        

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario  # Asegúrate de tener el modelo PerfilUsuario definido

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True, label="Nombre")
    second_name = forms.CharField(max_length=50, required=False, label="Segundo Nombre")
    last_name = forms.CharField(max_length=50, required=True, label="Apellido Paterno")
    second_last_name = forms.CharField(max_length=50, required=False, label="Apellido Materno")
    rut = forms.CharField(max_length=12, required=True, label="RUT")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'second_name', 'last_name', 'second_last_name', 'rut', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Crear perfil de usuario
            PerfilUsuario.objects.create(
                user=user,
                nombre=self.cleaned_data['first_name'],
                segundo_nombre=self.cleaned_data['second_name'],
                apellido_paterno=self.cleaned_data['last_name'],
                apellido_materno=self.cleaned_data['second_last_name'],
                rut=self.cleaned_data['rut'],
            )
        return user
