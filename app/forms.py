from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mensagem

class RegistroForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'As duas senhas não conferem.',
        'password_too_short': 'A senha deve ter pelo menos 8 caracteres.',
        'password_too_similar': 'A senha é muito similar ao nome de usuário.',
        'password_too_common': 'Essa senha é muito comum.',
        'password_entirely_numeric': 'A senha não pode ser totalmente numérica.'
    }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'Nome de usuário deve conter apenas letras, números e @/./+/-/_',
            'password1': 'A senha deve ter pelo menos 8 caracteres e não pode ser similar ao nome de usuário.',
            'password2': 'Digite a mesma senha para confirmação.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuário'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite sua mensagem...'
            })
        }
        labels = {
            'mensagem': 'Mensagem'
        }