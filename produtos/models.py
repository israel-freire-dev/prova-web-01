from django.db import models
from fornecedores.models import Fornecedor

# Create your models here.
class Produto(models.Model):
    # Identificação / Detalhes
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    codigo = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Código/SKU")
    categoria = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    unidade_medida = models.CharField(max_length=20, default="UN", verbose_name="Unidade de Medida")

    # Financeiro
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço de Custo")
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Preço de Venda")

    # Estoque
    quantidade = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0, verbose_name="Estoque Mínimo")
    data_validade = models.DateField(null=True, blank=True, verbose_name="Data de Validade")

    # Controle / Sistema
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    def __str__(self):
        return self.nome