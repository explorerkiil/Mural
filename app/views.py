from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Mensagem
from .forms import MensagemForm, RegistroForm

def mural(request):
    query = request.GET.get('q', '')
    if query:
        mensagens_por_data = Mensagem.objects.filter(
            Q(mensagem__icontains=query) | 
            Q(nome__icontains=query)
        ).order_by('-data')
        mensagens_por_upvotes = Mensagem.objects.filter(
            Q(mensagem__icontains=query) | 
            Q(nome__icontains=query)
        ).order_by('-upvotes', '-data')
    else:
        mensagens_por_data = Mensagem.objects.all().order_by('-data')
        mensagens_por_upvotes = Mensagem.objects.all().order_by('-upvotes', '-data')
    
    context = {
        'mensagens_por_data': mensagens_por_data,
        'mensagens_por_upvotes': mensagens_por_upvotes,
        'user': request.user,
        'query': query
    }
    return render(request, 'mural.html', context)

@login_required
def form(request):
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.nome = request.user.username
            mensagem.autor = request.user
            mensagem.save()
            return redirect('mural')
    else:
        form = MensagemForm()
    return render(request, 'form.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mural')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mural')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('mural')

@login_required
def upvote_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    
    if request.user in mensagem.upvoted_by.all():
        mensagem.upvotes -= 1
        mensagem.upvoted_by.remove(request.user)
        liked = False
    else:
        mensagem.upvotes += 1
        mensagem.upvoted_by.add(request.user)
        liked = True
    mensagem.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'upvotes': mensagem.upvotes,
            'liked': liked
        })
    return redirect('mural')

@login_required
def deletar_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    if request.user.is_superuser:
        mensagem.delete()
    return redirect('mural')