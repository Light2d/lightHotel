# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from .models import CustomUser  
from django.contrib.auth.forms import AuthenticationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Используем кастомную форму
        if form.is_valid():
            user = form.save()
            login(request, user)  # Войти сразу после регистрации
            messages.success(request, "Вы успешно зарегистрированы и авторизованы!")
            return redirect('index')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_banned:
                messages.error(request, "Вы заблокированы. Обратитесь к администратору.")
                return redirect('login')

            login(request, user)
            messages.success(request, "Вы успешно авторизовались")
            
            # Проверяем, нужно ли сменить пароль
            if user.last_login is None:
                return redirect('change_password')
                
            return redirect('index')
        else:
            # Отслеживаем количество неудачных попыток
            request.session['login_attempts'] = request.session.get('login_attempts', 0) + 1
            if request.session['login_attempts'] >= 3:
                # Блокируем пользователя после 3-х неудачных попыток
                user = CustomUser.objects.filter(username=username).first()
                if user:
                    user.is_banned = True
                    user.save()
                messages.error(request, "Вы заблокированы. Обратитесь к администратору.")
            else:
                messages.error(request, "Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введенные данные.")
            
            return redirect('login')

    # В случае GET запроса возвращаем форму
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Пароль успешно изменен.")
            return redirect('index')
        else:
            messages.error(request, "Ошибка при смене пароля. Проверьте введенные данные.")
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})