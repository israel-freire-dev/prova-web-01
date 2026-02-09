from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Produto
from .forms import ProdutoForm


# Create your views here.
class ProdutoListView(ListView):
    model = Produto
    template_name = "produtos/lista.html"
    context_object_name = "produtos"


class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/form.html"
    success_url = reverse_lazy("listar_produtos")


class ProdutoUpdateView(UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/form.html"
    success_url = reverse_lazy("listar_produtos")


class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = "produtos/excluir.html"
    success_url = reverse_lazy("listar_produtos")
