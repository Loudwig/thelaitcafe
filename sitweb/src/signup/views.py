from django.shortcuts import render
from signup.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def connexion(request):
    if request.method == 'POST':
        # Traitement du formulaire de connexion
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Rediriger l'utilisateur après la connexion réussie
                return redirect('boutique')  # Remplace 'accueil' par le nom de ta vue d'accueil
    else:
        form = CustomAuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

def creation_compte(request):
    if request.method == 'POST':
        # Traitement du formulaire de création de compte
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Rediriger l'utilisateur après la création de compte réussie
            return redirect('boutique')  # Remplace 'accueil' par le nom de ta vue d'accueil
    else:
        form = CustomUserCreationForm()
    return render(request, 'creation_compte.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('acceuil')