from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Profile
from django.contrib import messages
from .forms import ProfileUpdateForm, VerificationForm
from django.contrib.auth.decorators import login_required

@login_required
def account_verify(request):
    profile = request.user.profile

    if request.method == "POST":
        # Guardar las imágenes si se envían
        id_front = request.FILES.get("id_front")
        id_back = request.FILES.get("id_back")
        selfie_with_id = request.FILES.get("selfie_with_id")

        if id_front and id_back and selfie_with_id:
            profile.id_front = id_front
            profile.id_back = id_back
            profile.selfie_with_id = selfie_with_id
            profile.save()

            messages.success(request, "Imágenes enviadas correctamente. La verificación está pendiente.")
            return redirect("dashboard")  # Redirigir al dashboard

        else:
            messages.error(request, "Debes subir las tres imágenes para verificar tu cuenta.")

    return render(request, "account_verify.html")

def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProfileUpdateForm()

    return render(request, "profile.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard") 
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("login")  # Redirige al login tras cerrar sesión

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guarda el usuario y el perfil se creará automáticamente con signals.py
            user = form.save()  
            messages.success(request, "Registro exitoso. Inicia sesión.")
            return redirect("login")  
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

@login_required
def verify_account(request):
    profile = request.user.profile
    profile.is_verified = True  # Aquí podrías agregar lógica para verificación manual
    profile.save()
    return redirect("dashboard")
