from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.core.mail import send_mail
from django.conf import settings

def send(request):
    send_mail(
        'contact form',
        'Olá',
        'settings.EMAIL_HOST_USER',
        ['mateusfcvega@gmail.com', 'mateusggvega@gmail.com'],
        fail_silently=False
    )
    return HttpResponse("Olá")

def cadastro(request):
    if request.method == "GET":
        return render(request, 'login/cadastro.html', {'it': False})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return render(request, 'login/cadastro.html', {'it': True})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return render(request, 'login/login.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login/login.html', {'it': False})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(username=username, password=password)

        if user:
            lg(request, user)
            if not remember:
                request.session.set_expiry(0)
            return redirect('reader:mecanica')
        else:
            return render(request, 'login/login.html', {'it': True})
        
def saiba(request):
    return render(request, 'login/saiba.html')

def esqueci(request):
    return render(request, 'login/esqueci.html')