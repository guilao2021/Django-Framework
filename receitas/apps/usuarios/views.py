from receitas.models import Receita
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages

def cadastro(request):
    """Cadastra novo usuário no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome) or campo_vazio(email):
            messages.error(request, 'O campo não deve ficar em branco!')            
            return redirect('cadastro')        
        if senha != senha2:
            messages.error(request, 'As senhas não são iguais')           
            return redirect('cadastro')
        if usuario_ja_cadastrado(nome) or email_ja_cadastrado(email):
            messages.error(request, 'Usuário já cadastrado')            
            return redirect('cadastro')
        user = User.objects.create_user(username = nome, email = email, password = senha)
        user.save()         
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('login')   
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o Login do usuário no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'O email e a senha não podem ficar em branco')             
            return redirect('login')
        if User.objects.filter(email = email).exists():
            nome = User.objects.filter(email = email).values_list('username', flat = True).get()
            user = auth.authenticate(request, username = nome, password = senha)
            if user is not None:
                auth.login(request, user)                                
                return redirect('dashboard')      
    return render(request, 'usuarios/login.html')

def logout(request):
    """Realiza o Logout do usuário"""
    auth.logout(request)    
    return redirect('index')
    
def dashboard(request):
    """Página inicial do usuário logado"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa = id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    """Inválida campos não preenchidos"""
    return not campo.strip()

def usuario_ja_cadastrado(campo):
    """Inválida cadastros com nome de usuários já existentes"""
    return User.objects.filter(username = campo).exists()

def email_ja_cadastrado(campo):
    """Inválida cadastros com emails já existentes"""
    return User.objects.filter(email = campo).exists()
