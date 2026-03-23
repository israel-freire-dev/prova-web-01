from rest_framework import serializers

from .models import Compra, CompraFornecedor, ItemCompra


class ItemCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ["id", "produto", "quantidade", "preco_unitario", "compra_fornecedor"]


class CompraFornecedorSerializer(serializers.ModelSerializer):
    itens = ItemCompraSerializer(many=True, read_only=True)

    class Meta:
        model = CompraFornecedor
        fields = ["id", "compra", "fornecedor", "itens"]


class CompraSerializer(serializers.ModelSerializer):
    grupos = CompraFornecedorSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "data", "status", "grupos", "created_at", "updated_at"]

