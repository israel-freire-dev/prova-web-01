from django.urls import path
from . import views

from .views import (
    FornecedorCreateView,
    FornecedorDeleteView,
    FornecedorListView,
    FornecedorUpdateView,
)


urlpatterns = [
    path("fornecedores/", FornecedorListView.as_view(), name="listar_fornecedores"),
    path("fornecedores/adicionar/", FornecedorCreateView.as_view(), name="criar_fornecedor"),
    path("fornecedores/editar/<int:pk>/", FornecedorUpdateView.as_view(), name="editar_fornecedor"),
    path("fornecedores/excluir/<int:pk>/", FornecedorDeleteView.as_view(), name="excluir_fornecedor"),

    # --- API Views ---
    path("public/fornecedores/", views.get_fornecedores, name="get_fornecedores"),
    path("public/fornecedores/<int:pk>/", views.get_fornecedor, name="get_fornecedor"),
    path("public/fornecedores/criar/", views.post_fornecedor, name="post_fornecedor"),
    path("public/fornecedores/<int:pk>/editar/", views.put_fornecedor, name="put_fornecedor"),
    path("public/fornecedores/<int:pk>/excluir/", views.delete_fornecedor, name="delete_fornecedor"),
]
