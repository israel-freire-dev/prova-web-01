from django.contrib import admin

from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "cidade", "estado", "cnpj", "is_active")
    list_filter = ("is_active", "estado", "categoria")
    search_fields = ("nome", "cnpj", "email", "telefone", "cidade")
