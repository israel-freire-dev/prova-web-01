from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Fornecedor
from rest_framework.decorators import api_view
from .serializers import FornecedorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


# Create your views here.
class FornecedorListView(ListView):
    model = Fornecedor
    template_name = "fornecedores/lista.html"
    context_object_name = "fornecedores"


class FornecedorCreateView(CreateView):
    model = Fornecedor
    fields = ("nome", "telefone", "email", "categoria", "cidade", "estado", "cnpj", "is_active")
    template_name = "fornecedores/form.html"
    success_url = reverse_lazy("listar_fornecedores")


class FornecedorUpdateView(UpdateView):
    model = Fornecedor
    fields = ("nome", "telefone", "email", "categoria", "cidade", "estado", "cnpj", "is_active")
    template_name = "fornecedores/form.html"
    success_url = reverse_lazy("listar_fornecedores")


class FornecedorDeleteView(DeleteView):
    model = Fornecedor
    template_name = "fornecedores/excluir.html"
    success_url = reverse_lazy("listar_fornecedores")


#django rest_framework

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


@api_view(['GET'])
def get_fornecedores(request):

    if request.method == 'GET': 
       fornecedores = Fornecedor.objects.all()
       serializer = FornecedorSerializer(fornecedores, many=True)
       return Response(serializer.data)

    return Response(status.HTTP_404_NOT_FOUND)
