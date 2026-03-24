from django.db import models
from django.utils import timezone
# Create your models here.
class Cliente(models.Model):
    # Escolhas para Estados (UF)
    ESTADOS_CHOICES = [
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
        ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
        ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
        ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
        ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
        ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')
    ]

    # Dados Pessoais / Identificação
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", default=None)
    telefone = models.CharField(max_length=15, blank=True)
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")

    # Endereço
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    endereco = models.CharField(max_length=200, blank=True, verbose_name="Endereço")
    numero = models.CharField(max_length=10, blank=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES, blank=True)

    # Controle / Sistema
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    def __str__(self):
        return self.nome