from django.contrib import admin

from .models import Compra, CompraFornecedor, ItemCompra


class CompraFornecedorInline(admin.TabularInline):
    model = CompraFornecedor
    extra = 0


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "data", "status", "created_at", "updated_at")
    list_filter = ("status", "data")
    inlines = [CompraFornecedorInline]


class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 0


@admin.register(CompraFornecedor)
class CompraFornecedorAdmin(admin.ModelAdmin):
    list_display = ("id", "compra", "fornecedor")
    inlines = [ItemCompraInline]


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ("id", "compra_fornecedor", "produto", "quantidade", "preco_unitario")
