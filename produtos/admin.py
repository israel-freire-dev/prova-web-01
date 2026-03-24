from django.contrib import admin

from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco_venda", "quantidade", "data_validade")
    list_filter = ("data_validade",)
    search_fields = ("nome",)
