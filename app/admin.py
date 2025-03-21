from django.contrib import admin
from .models import Mensagem

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'autor', 'data', 'upvotes')
    list_filter = ('data', 'autor')
    search_fields = ('nome', 'mensagem')
    ordering = ('-data',)