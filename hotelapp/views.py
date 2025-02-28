# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import user_passes_test
from .forms import UserForm
from .models import CustomUser
from django.shortcuts import get_object_or_404


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            user = form.save()
            login(request, user)  
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
            
            if user.last_login is None:
                return redirect('change_password')
                
            return redirect('index')
        else:
            request.session['login_attempts'] = request.session.get('login_attempts', 0) + 1
            if request.session['login_attempts'] >= 3:
                user = CustomUser.objects.filter(username=username).first()
                if user:
                    user.is_banned = True
                    user.save()
                messages.error(request, "Вы заблокированы. Обратитесь к администратору.")
            else:
                messages.error(request, "Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введенные данные.")
            
            return redirect('login')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def aboutUs(request):
    return render(request, 'about.html')

@login_required
def contacts(request):
    return render(request, 'contact.html')

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


def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно добавлен.")
            return redirect('user_list') 
        else:
            messages.error(request, "Ошибка при добавлении пользователя.")
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные пользователя успешно обновлены.")
            return redirect('user_list')
        else:
            messages.error(request, "Ошибка при обновлении данных пользователя.")
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})


@user_passes_test(is_admin)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


def ban_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_banned = True
    user.save()

    messages.success(request, f'Пользователь {user.username} был заблокирован.')
    return redirect('user_list') 

def unban_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if user.is_banned:
        user.is_banned = False
        user.save()
        messages.success(request, f'Пользователь {user.username} разблокирован.')
    else:
        messages.info(request, f'Пользователь {user.username} уже не заблокирован.')
    
    return redirect('user_list')