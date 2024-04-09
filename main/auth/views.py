from django.shortcuts import render, redirect
from main import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('front:index')
            else:
                return render(request,'front/auth/login.html')
        except:
            return redirect('login')
    return render(request, 'front/auth/login.html')

def register(request):
    if request.method == 'POST':
        try:
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                models.User.objects.create_user(
                    username=username, 
                    password=password, 
                    first_name=f_name, 
                    last_name=l_name
                    )
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('front:index')
        except:
            return redirect('front:register')
    return render(request, 'front/auth/register.html')

def log_out(request):
    logout(request)
    return redirect('front:index')

@login_required(login_url='auth:login')
def profile(request):
    if request.method == 'POST':
        username = request.user.username
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('new_password_confirm')
        if authenticate(username=username,password=password):
            user = models.User.objects.get(username=username)
            user.first_name = f_name if f_name else ''
            user.last_name = l_name if l_name else ''
            user.email = email if email else ''
            if new_password and new_password == new_password_confirm:
                user.set_password(new_password)
            user.save()
            return redirect('auth:profile')
        # return redirect('front:profile')
    return render(request, 'front/auth/profile.html')


@login_required(login_url='auth:login')
def carts(request):
    queryset = models.Cart.objects.filter(user=request.user, is_active=False)
    context = {'queryset':queryset}
    return render(request, 'front/carts/list.html', context)