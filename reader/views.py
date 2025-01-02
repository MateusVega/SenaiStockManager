from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import mecanica, eletrica, eletronica, eventos
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
import pandas as pd
import datetime

data = datetime.datetime.now()
data = data - datetime.timedelta(days=1)
data = data.date()

@login_required(login_url='login')
def time(request):
    return render(request, 'reader/times.html')

@login_required(login_url='login')
def mecanicas(request):
    user = request.user
    role = user.is_staff
    return render(request, 'reader/index.html', {'ferramentas': mecanica.objects.all().values(), 'tabela' : 'mecanica', 'evento': eventos.objects.filter(user=request.user).values(), 'user' : user, 'role' : role, 'it' : '', 'data' : data})

@login_required(login_url='login')
def eletricas(request):
    user = request.user
    role = user.is_staff
    return render(request, 'reader/index.html', {'ferramentas': eletrica.objects.all().values(), 'tabela' : 'eletrica', 'evento': eventos.objects.filter(user=request.user).values(), 'user' : user, 'role' : role, 'it' : '', 'data' : data})

@login_required(login_url='login')
def eletronicas(request):
    user = request.user
    role = user.is_staff
    return render(request, 'reader/index.html', {'ferramentas': eletronica.objects.all().values(), 'tabela' : 'eletronica', 'evento': eventos.objects.filter(user=request.user).values(), 'user' : user, 'role' : role, 'it' : '', 'data' : data})

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='login')
def add(request):
    return render(request, 'reader/add.html')

@login_required(login_url='login')
@csrf_exempt
def save_qr_data(request):
    if request.method == "POST":
        tabela = request.POST.get("tabela")
        if tabela == "mecanica":
            ferramenta = mecanica()
        elif tabela == "eletrica":
            ferramenta = eletrica()
        else:
            ferramenta = eletronica()

        ferramenta.numero = request.POST.get("numero")
        ferramenta.nome = request.POST.get("nome")
        ferramenta.local = request.POST.get("local")
        ferramenta.instrutor = request.POST.get("instrutor")
        ferramenta.status = "off"
        ferramenta.save()
        return redirect('reader:add')

@login_required(login_url='login')
@csrf_exempt
def off_to_on(request):
    if request.method == "POST":
        decodetext = request.POST.get("decodetext")
        tabela = request.POST.get('tabela')
        user = request.user
        role = user.is_staff

        if mecanica.objects.filter(numero=decodetext).exists():
            tabela_encontrada = "mecanica"
            if tabela == tabela_encontrada:
                mecanica.objects.filter(numero=decodetext).update(status="on")
                return redirect('reader:mecanica')
        elif eletrica.objects.filter(numero=decodetext).exists():
            tabela_encontrada = "eletrica"
            if tabela == tabela_encontrada:
                eletrica.objects.filter(numero=decodetext).update(status="on")
                return redirect('reader:eletrica')
        elif eletronica.objects.filter(numero=decodetext).exists():
            tabela_encontrada = "eletronica"
            if tabela == tabela_encontrada:
                eletronica.objects.filter(numero=decodetext).update(status="on")
                return redirect('reader:eletronica')
        else:
            tabela_encontrada = "not"
            return redirect('reader:mecanica')

        if decodetext:
            if tabela == "mecanica":
                return render(request, 'reader/index.html', {'ferramentas': mecanica.objects.all().values(), 'tabela' : 'mecanica', 'evento': eventos.objects.filter(user=request.user).values(), 'user' : user, 'role' : role, 'it' : tabela_encontrada, 'data' : data})
            elif tabela == "eletrica":
                return render(request, 'reader/index.html', {'ferramentas': eletrica.objects.all().values(), 'tabela' : 'eletrica', 'evento': eventos.objects.filter(user=request.user).values(), 'user' : user, 'role' : role, 'it' : tabela_encontrada, 'data' : data})
            else:
                return render(request, 'reader/index.html', {'ferramentas': eletronica.objects.all().values(), 'tabela' : 'eletronica', 'evento': eventos.objects.filter(user=request.user).values(), 'user' : user, 'role' : role, 'it' : tabela_encontrada, 'data' : data})

@login_required(login_url='login')
def reset(request, tabela):
    if tabela == "mecanica":
        mecanica.objects.filter(status="on").update(status="off")
        return redirect('reader:mecanica')
    elif tabela == "eletrica":
        eletrica.objects.filter(status="on").update(status="off")
        return redirect('reader:eletrica')
    else:
        eletronica.objects.filter(status="on").update(status="off")
        return redirect('reader:eletronica')

        
@login_required(login_url='login')
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        evento = request.POST.get('evento')
        eventos.objects.create(data=data, evento=evento, user=request.user)
        return redirect('reader:mecanica')

@login_required(login_url='login')
@csrf_exempt
def remove_event(request, id):
    eventos.objects.filter(id=id).delete()
    return redirect('reader:mecanica')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@csrf_exempt
def transfer(request, tabela):
    if request.method == 'POST':
        tabela_origem = request.POST.get('tabela')
        number = request.POST.get('number')

        tabelas = {
            "mecanica": mecanica,
            "eletrica": eletrica,
            "eletronica": eletronica
        }


        modelo_origem = tabelas[tabela]
        modelo_destino = tabelas[tabela_origem]

        objeto = modelo_origem.objects.get(numero=number)
        
        modelo_destino.objects.create(**{
            field.name: getattr(objeto, field.name)
            for field in modelo_origem._meta.fields
            if field.name != 'id'
        })
        
        objeto.delete()

        return redirect(f'reader:{tabela}')

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='login')
def xlsx(request):
    return render(request, 'reader/xlsx.html', {'ferramentas': mecanica.objects.all().values(), 'tabela' : 'mecanica'})

def upload_file(request):
    if request.method == 'POST':
        table = request.POST.get('table')
        file = request.FILES.get('file')
        df = pd.read_excel(file)
        model = {
            'mecanica': mecanica,
            'eletrica': eletrica,
            'eletronica': eletronica
        }.get(table)
        for _, row in df.iterrows():
            model.objects.update_or_create(
                numero=row[0],
                defaults={
                    'nome': row[1],
                    'local': row[2],
                    'instrutor': row[3],
                    'status': "off"
                }
            )
        return redirect(f'reader:{table}')