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
    path("fornecedores/public/api/", views.get_fornecedores, name="get_fornecedores"),
]
