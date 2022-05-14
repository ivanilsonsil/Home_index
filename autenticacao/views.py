from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
#  importando mensagens de erro para usuário
from django.contrib import messages 
from django.contrib.messages import constants 
from django.contrib import auth # IMPORTANDO A AUTENTICAÇÃO PARA LOGAR
# Create your views here.

def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated: # se o usuário está autenticado derecioner ele para plataforma
            return redirect('/plataforma')

        return  render(request,'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("password")
        confirmar_senha = request.POST.get("confirm-password")

        #Validação
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/auth/cadastro')

        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')

        user = User.objects.filter(username = username)

        if user.exists ():
            messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
            return redirect('/auth/cadastro')
            
        #TRATAMENTO DE ERROS.. 
        try:
            
            
            user = User.objects.create_user(username = username, password = senha)
            user.save  #SALVANDO NO BANCO DE DADOS
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return redirect('/auth/logar') # se o usuário cadastrou redirecinar ele
            #para o login

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro') # CASO DE ERRO REDIRECIONAR PARA CADASTRO

# FUNCÇÃO LOGAR

def logar(request):
    if request.method =="GET": 
        if request.user.is_authenticated: # se o usuário está autenticado derecioner ele para plataforma
            return redirect('/plataforma')

        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = auth.authenticate(username=username, password=senha)

        
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/logar')
        else:
             auth.login(request, usuario)
             return redirect('/plataforma')

def sair(request):
    auth.logout(request) # obs
    return redirect('/auth/logar')       
