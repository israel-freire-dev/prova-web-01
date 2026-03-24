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
    produtos = Produto.objects.all()
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_produto(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProdutoSerializer(produto)
    return Response(serializer.data)


@api_view(['POST'])
def post_produto(request):
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_produto(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProdutoSerializer(produto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_produto(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    produto.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)