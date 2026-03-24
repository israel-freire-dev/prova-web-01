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


@api_view(['GET'])
def get_fornecedores(request):

    if request.method == 'GET': 
       fornecedores = Fornecedor.objects.all()
       serializer = FornecedorSerializer(fornecedores, many=True)
       return Response(serializer.data)

    return Response(status.HTTP_404_NOT_FOUND)
