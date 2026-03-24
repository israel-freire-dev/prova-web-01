from django.urls import path

from . import views

urlpatterns = [
    # --- Template Views ---
    path("compras/", views.CompraListView.as_view(), name="listar_compras"),
    path("compras/adicionar/", views.CompraCreateView.as_view(), name="criar_compra"),
    path("compras/<int:pk>/", views.CompraDetailView.as_view(), name="detalhes_compra"),
    path("compras/editar/<int:pk>/", views.CompraUpdateView.as_view(), name="editar_compra"),
    path("compras/excluir/<int:pk>/", views.CompraDeleteView.as_view(), name="excluir_compra"),
    
    # Ações da Compra
    path("compras/<int:compra_pk>/adicionar-item/", views.adicionar_item, name="adicionar_item"),
    path("compras/<int:compra_pk>/remover-item/<int:item_pk>/", views.remover_item, name="remover_item"),
    path("compras/<int:pk>/confirmar/", views.confirmar_compra_view, name="confirmar_compra_view"),
    path("compras/<int:pk>/confirmar-entrega/", views.confirmar_entrega_view, name="confirmar_entrega_view"),
    path("compras/<int:pk>/cancelar/", views.cancelar_compra_view, name="cancelar_compra_view"),

    # Endpoint AJAX
    path("api/fornecedores/<int:fornecedor_id>/produtos/", views.get_produtos_fornecedor_api, name="api_produtos_fornecedor"),

    # --- API Views ---
    path("public/compras/", views.get_compras, name="get_compras"),
    path(
        "public/compras/<int:compra_id>/confirmar/",
        views.post_confirmar_compra,
        name="confirmar_compra",
    ),
    path(
        "public/compras/<int:compra_id>/cancelar/",
        views.post_cancelar_compra,
        name="cancelar_compra",
    ),
]

