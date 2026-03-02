from rest_framework import serializers
from .models import Fornecedor


class FornecedorSerializer(serializers.ModelSerializer):
  class Meta:
     model = Fornecedor
     fields = ['nome', 'telefone', 'email', 'categoria', 'cidade', 'estado', 'cnpj', 'is_active']
