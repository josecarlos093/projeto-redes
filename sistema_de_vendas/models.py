from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    tempo_cadastro = models.DateField(auto_now_add=True)
    usuario = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=50)

    def __str__(self):
        return self.nome