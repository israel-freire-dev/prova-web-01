from django.urls import path
from . import views
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView
)

urlpatterns = [
    path("clientes/", ClienteListView.as_view(), name="listar_clientes"),
    path("clientes/adicionar/", ClienteCreateView.as_view(), name="criar_cliente"),
    path("clientes/editar/<int:pk>/", ClienteUpdateView.as_view(), name="editar_cliente"),
    path("clientes/excluir/<int:pk>/", ClienteDeleteView.as_view(), name="excluir_cliente"),
    path("clientes/public/api/", views.get_clientes, name='get_clientes')
]