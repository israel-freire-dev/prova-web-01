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

    # --- API Views ---
    path("public/clientes/", views.get_clientes, name='get_clientes'),
    path("public/clientes/<int:pk>/", views.get_cliente, name='get_cliente'),
    path("public/clientes/criar/", views.post_cliente, name='post_cliente'),
    path("public/clientes/<int:pk>/editar/", views.put_cliente, name='put_cliente'),
    path("public/clientes/<int:pk>/excluir/", views.delete_cliente, name='delete_cliente'),
]