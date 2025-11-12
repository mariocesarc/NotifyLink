from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from core.models import SubscriptionPlan


User = get_user_model()


def main_page(request):
    if request.user.is_authenticated:
        return redirect('config_page')
    plans = SubscriptionPlan.objects.order_by('price')
    return render(request, 'core/main.html', {'plans': plans})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('config_page')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username:
            error = 'El username es obligatorio'
        elif not password:
            error = 'La contraseña es obligatoria'
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('config_page')
            else:
                error = 'Username o contraseña incorrectos'
        
        context = {
            'error': error,
            'username': username
        }
        return render(request, 'core/sign_in.html', context)
    
    return render(request, 'core/sign_in.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('config_page')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        RESERVED_USERNAMES = {'admin', 'static', 'sign_in', 'sign_up', 'media', 'config', 'analytics'}
        
        # validaciones
        if not username:
            error = 'El username es obligatorio'
        elif username in RESERVED_USERNAMES:
            error = 'El username no puede ser {}, esta reservado'.format(username)
        elif not display_name:
            error = 'El display name es obligatorio'
        elif not password1:
            error = 'La contraseña es obligatoria'
        elif password1 != password2:
            error = 'Las contraseñas no coinciden'
        elif len(password1) < 8:
            error = 'La contraseña debe tener al menos 8 caracteres'
        elif User.objects.filter(username=username).exists():
            error = 'Este username ya está en uso'
        else:
            error = None
            
        if error:
            context = {
                'error': error,
                'username': username,
                'display_name': display_name
            }
            return render(request, 'core/sign_up.html', context)

        user = User.objects.create_user(
            username=username,
            password=password1,
            display_name=display_name
        )

        login(request, user)

        return redirect('config_page')
    
    return render(request, 'core/sign_up.html')


@require_POST
def log_out(request):
    logout(request)
    return redirect('main_page')
