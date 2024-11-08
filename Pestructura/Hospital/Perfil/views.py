from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .models import  Perfil
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'home.html')



def index(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'index.html')


def login_view(request):
    error = ""  # Inicializa la variable de error

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verifica si el usuario tiene el permiso de 'staff' (solo ejemplo)
            if user.is_staff:
                login(request, user)
                try:
                    # Obtiene el rol del usuario
                    rol = user.perfil.rol
                    error = "no"

                    # Redirige a diferentes páginas según el rol
                    if rol == 'enfermero':
                        return redirect('enfermero_dashboard')
                    elif rol == 'doctor':
                        return redirect('doctor_dashboard')
                    elif rol == 'administrador':
                        return redirect('admin_dashboard')
                except Perfil.DoesNotExist:
                    error = "yes"  # Si no tiene perfil, muestra error
            else:
                error = "yes"
        else:
            error = "yes"

    d = {'error': error}
    return render(request, 'login.html', d)

def logout_view(request):
    if not request.user.is_staff:
        return redirect('index')

    logout(request)
    return redirect('index')




@login_required
def enfermero_dashboard(request):
    return render(request, 'enfermero_dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

