from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    ci = forms.IntegerField(required=True, label="Carnet de Identidad", widget=forms.NumberInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']  # Quita 'ci'

    def clean_ci(self):
        ci = self.cleaned_data.get('ci')

        if Profile.objects.filter(ci=ci).exists():  # Cambia User por Profile
            raise forms.ValidationError("Este Carnet de Identidad ya está registrado.")

        return ci
    
def save(self, commit=True):
    user = super().save(commit=False)  # Guarda el usuario sin enviarlo aún a la BD
    user.email = self.cleaned_data.get('email')
    user.first_name = self.cleaned_data.get('first_name')
    user.last_name = self.cleaned_data.get('last_name')
    
    if commit:
        user.save()  # Guarda el usuario en la BD
        Profile.objects.create(user=user, ci=self.cleaned_data['ci'])  # Crea el perfil

    return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class VerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["id_front", "id_back", "selfie_with_id"]
        widgets = {
            "id_front": forms.FileInput(attrs={"accept": "image/*", "class": "block w-full"}),
            "id_back": forms.FileInput(attrs={"accept": "image/*", "class": "block w-full"}),
            "selfie_with_id": forms.FileInput(attrs={"accept": "image/*", "class": "block w-full"}),
        }