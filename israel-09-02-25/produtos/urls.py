from django.urls import path
from .views import (
    ProdutoListView,
    ProdutoCreateView,
    ProdutoUpdateView,
    ProdutoDeleteView
)


urlpatterns = [
    path("produtos/", ProdutoListView.as_view(), name="listar_produtos"),
    path("produtos/adicionar/", ProdutoCreateView.as_view(), name="criar_produto"),
    path("produtos/editar/<int:pk>/", ProdutoUpdateView.as_view(), name="editar_produto"),
    path("produtos/excluir/<int:pk>/", ProdutoDeleteView.as_view(), name="excluir_produto"),
]