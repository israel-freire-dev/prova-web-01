from django.db import models

class Fornecedor(models.Model):
    ESTADOS_CHOICES = (
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
        ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
        ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
        ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
        ('SE', 'SE'), ('TO', 'TO')
    )

    # Identificação Primária
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, blank=True)
    categoria = models.CharField(max_length=100, blank=True)

    # Contatos e Web
    telefone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    site = models.URLField(blank=True, null=True)
    nome_representante = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nome do Representante")

    # Endereço Completo
    cep = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=150, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES, blank=True)

    # Dados Bancários
    banco = models.CharField(max_length=100, blank=True, null=True)
    agencia = models.CharField(max_length=20, blank=True, null=True)
    conta = models.CharField(max_length=20, blank=True, null=True)
    chave_pix = models.CharField(max_length=150, blank=True, null=True)

    # Sistema / Controle
    is_active = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True)
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    def __str__(self) -> str:
        return self.nome
