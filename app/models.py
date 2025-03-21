from django.db import models
from django.contrib.auth.models import User

class Mensagem(models.Model):
    nome = models.CharField(max_length=100)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_messages', blank=True)

    def __str__(self):
        return f"{self.nome} - {self.data.strftime('%d/%m/%Y %H:%M')}"