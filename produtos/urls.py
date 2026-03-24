from django.urls import path
from . import views
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

    # --- API Views ---
    path("public/produtos/", views.get_produtos, name='get_produtos'),
    path("public/produtos/<int:pk>/", views.get_produto, name='get_produto'),
    path("public/produtos/criar/", views.post_produto, name='post_produto'),
    path("public/produtos/<int:pk>/editar/", views.put_produto, name='put_produto'),
    path("public/produtos/<int:pk>/excluir/", views.delete_produto, name='delete_produto'),
]