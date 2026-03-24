from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Fornecedor
from .forms import FornecedorForm
from rest_framework.decorators import api_view
from .serializers import FornecedorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema


# Create your views here.
class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = "fornecedores/lista.html"
    context_object_name = "fornecedores"


class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = "fornecedores/form.html"
    success_url = reverse_lazy("listar_fornecedores")


class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = "fornecedores/form.html"
    success_url = reverse_lazy("listar_fornecedores")


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = "fornecedores/excluir.html"
    success_url = reverse_lazy("listar_fornecedores")


#django rest_framework

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


@extend_schema(tags=['Fornecedores'])
@api_view(['GET'])
def get_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    serializer = FornecedorSerializer(fornecedores, many=True)
    return Response(serializer.data)


@extend_schema(tags=['Fornecedores'])
@api_view(['GET'])
def get_fornecedor(request, pk):
    try:
        fornecedor = Fornecedor.objects.get(pk=pk)
    except Fornecedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FornecedorSerializer(fornecedor)
    return Response(serializer.data)


@extend_schema(tags=['Fornecedores'], request=FornecedorSerializer, responses=FornecedorSerializer)
@api_view(['POST'])
def post_fornecedor(request):
    serializer = FornecedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Fornecedores'], request=FornecedorSerializer, responses=FornecedorSerializer)
@api_view(['PUT'])
def put_fornecedor(request, pk):
    try:
        fornecedor = Fornecedor.objects.get(pk=pk)
    except Fornecedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FornecedorSerializer(fornecedor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Fornecedores'])
@api_view(['DELETE'])
def delete_fornecedor(request, pk):
    try:
        fornecedor = Fornecedor.objects.get(pk=pk)
    except Fornecedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    fornecedor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
