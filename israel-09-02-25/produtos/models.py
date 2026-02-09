from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    quantidade = models.IntegerField()
    data_validade = models.DateField()


    def __str__(self):
        return self.nome