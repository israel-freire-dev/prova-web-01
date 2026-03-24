from rest_framework import serializers

from .models import Compra, ItemCompra


class ItemCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ["id", "produto", "quantidade", "preco_unitario", "compra"]


class CompraSerializer(serializers.ModelSerializer):
    itens = ItemCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "fornecedor", "data", "status", "itens", "created_at", "updated_at"]

