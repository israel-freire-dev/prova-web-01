from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=100, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nome
