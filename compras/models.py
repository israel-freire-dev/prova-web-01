from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from fornecedores.models import Fornecedor
from produtos.models import Produto


class Compra(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = "RASCUNHO", "Rascunho"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        CANCELADA = "CANCELADA", "Cancelada"

    data = models.DateField(verbose_name="Data da compra", default=timezone.now)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, verbose_name="Fornecedor")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RASCUNHO,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Compra #{self.pk or 'novo'} ({self.get_status_display()}) - {self.data}"

    @property
    def is_editable(self) -> bool:
        return self.status == self.Status.RASCUNHO


class ItemCompra(models.Model):
    compra = models.ForeignKey(
        Compra, on_delete=models.CASCADE, related_name="itens", null=True
    )
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(
        verbose_name="Quantidade",
        validators=[MinValueValidator(1, "A quantidade deve ser maior ou igual a 1")],
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "O preço unitário deve ser maior que zero")],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["compra", "produto"],
                name="uniq_item_por_produto_na_compra",
            )
        ]

    def __str__(self) -> str:
        return f"{self.produto} x{self.quantidade}"

    def clean(self) -> None:
        super().clean()
        if self.compra and not self.compra.is_editable:
            raise ValidationError("Não é possível alterar itens em compra não rascunho.")