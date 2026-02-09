from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm


# Create your views here.
class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/lista.html"
    context_object_name = "clientes"


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("listar_clientes")  



class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("listar_clientes")


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "clientes/excluir.html"
    success_url = reverse_lazy("listar_clientes")