from django.contrib import admin

from .models import Compra, ItemCompra


class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 0


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "fornecedor", "data", "status", "created_at", "updated_at")
    list_filter = ("status", "data", "fornecedor")
    inlines = [ItemCompraInline]


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ("id", "compra", "produto", "quantidade", "preco_unitario")
