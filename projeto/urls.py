from django.contrib import admin
from django.urls import path
from app.views import mural, form, login_view, registro_view, logout_view, deletar_mensagem, upvote_mensagem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mural, name='mural'),
    path('form/', form, name='form'),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', logout_view, name='logout'),
    path('deletar_mensagem/<int:mensagem_id>/', deletar_mensagem, name='deletar_mensagem'),
    path('upvote_mensagem/<int:mensagem_id>/', upvote_mensagem, name='upvote_mensagem'),
]