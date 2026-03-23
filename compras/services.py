from __future__ import annotations

from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from produtos.models import Produto

from .models import Compra, ItemCompra


def _listar_itens(compra: Compra) -> list[ItemCompra]:
    return list(
        ItemCompra.objects.select_related(
            "produto",
            "compra_fornecedor",
            "compra_fornecedor__fornecedor",
            "compra_fornecedor__compra",
        )
        .filter(compra_fornecedor__compra=compra)
        .order_by(
            "compra_fornecedor__fornecedor_id",
            "produto_id",
            "id",
        )
    )


@transaction.atomic
def confirmar_compra(compra_id: int) -> Compra:
    compra = Compra.objects.select_for_update().get(pk=compra_id)

    if compra.status != Compra.Status.RASCUNHO:
        raise ValidationError("A compra precisa estar em RASCUNHO para ser confirmada.")

    itens = _listar_itens(compra)
    if not itens:
        raise ValidationError("Não é possível confirmar uma compra sem itens.")

    produto_ids = sorted({i.produto_id for i in itens})
    Produto.objects.select_for_update().filter(id__in=produto_ids).order_by("id")

    quantidades_por_produto: dict[int, int] = defaultdict(int)
    for item in itens:
        quantidades_por_produto[item.produto_id] += int(item.quantidade)

    for produto_id, qtd in quantidades_por_produto.items():
        Produto.objects.filter(pk=produto_id).update(quantidade=F("quantidade") + qtd)

    compra.status = Compra.Status.CONFIRMADA
    compra.save(update_fields=["status", "updated_at"])
    return compra


@transaction.atomic
def cancelar_compra(compra_id: int) -> Compra:
    compra = Compra.objects.select_for_update().get(pk=compra_id)

    if compra.status == Compra.Status.CANCELADA:
        raise ValidationError("A compra já está CANCELADA.")

    if compra.status == Compra.Status.RASCUNHO:
        compra.status = Compra.Status.CANCELADA
        compra.save(update_fields=["status", "updated_at"])
        return compra

    if compra.status != Compra.Status.CONFIRMADA:
        raise ValidationError("Status inválido para cancelamento.")

    itens = _listar_itens(compra)
    produto_ids = sorted({i.produto_id for i in itens})
    produtos = (
        Produto.objects.select_for_update()
        .filter(id__in=produto_ids)
        .in_bulk(field_name="id")
    )

    quantidades_por_produto: dict[int, int] = defaultdict(int)
    for item in itens:
        quantidades_por_produto[item.produto_id] += int(item.quantidade)

    for produto_id, qtd in quantidades_por_produto.items():
        produto = produtos.get(produto_id)
        if produto is None:
            raise ValidationError("Produto inexistente para estorno.")
        if produto.quantidade - qtd < 0:
            raise ValidationError(
                f"Cancelamento deixaria estoque negativo para '{produto.nome}'."
            )

    for produto_id, qtd in quantidades_por_produto.items():
        Produto.objects.filter(pk=produto_id).update(quantidade=F("quantidade") - qtd)

    compra.status = Compra.Status.CANCELADA
    compra.save(update_fields=["status", "updated_at"])
    return compra

