from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Produto
from .forms import ProdutoForm
from rest_framework.decorators import api_view
from .serializers import ProdutoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

# Create your views here.
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "produtos/lista.html"
    context_object_name = "produtos"


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/form.html"
    success_url = reverse_lazy("listar_produtos")


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "produtos/form.html"
    success_url = reverse_lazy("listar_produtos")


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "produtos/excluir.html"
    success_url = reverse_lazy("listar_produtos")


#django rest_framework

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


@api_view(['GET'])
def get_produtos(request):

    if request.method == 'GET': 
       produtos = Produto.objects.all()
       serializer = ProdutoSerializer(produtos, many=True)
       return Response(serializer.data)

    return Response(status.HTTP_404_NOT_FOUND)