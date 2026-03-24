from django.contrib import messages  # pyright: ignore[reportMissingImports]
from django.core.exceptions import ValidationError  # pyright: ignore[reportMissingImports]
from django.shortcuts import get_object_or_404, redirect  # pyright: ignore[reportMissingImports]
from django.urls import reverse_lazy  # pyright: ignore[reportMissingImports]
from django.views.decorators.http import require_POST  # pyright: ignore[reportMissingImports]
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView  # pyright: ignore[reportMissingImports]
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from rest_framework import status  # pyright: ignore[reportMissingImports]
from rest_framework.decorators import api_view  # pyright: ignore[reportMissingImports]
from rest_framework.response import Response  # pyright: ignore[reportMissingImports]

from .forms import CompraForm, CompraFornecedorForm, ItemCompraForm
from .models import Compra, CompraFornecedor, ItemCompra
from .serializers import CompraSerializer
from .services import cancelar_compra, confirmar_compra


# --- API Views ---

@api_view(["GET"])
def get_compras(request):
    compras = Compra.objects.all().order_by("-id")
    serializer = CompraSerializer(compras, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def post_confirmar_compra(request, compra_id: int):
    try:
        compra = confirmar_compra(compra_id)
    except Compra.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    return Response(CompraSerializer(compra).data)


@api_view(["POST"])
def post_cancelar_compra(request, compra_id: int):
    try:
        compra = cancelar_compra(compra_id)
    except Compra.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    return Response(CompraSerializer(compra).data)


# --- Template Views ---

class CompraListView(LoginRequiredMixin, ListView):
    model = Compra
    template_name = "compras/lista.html"
    context_object_name = "compras"
    ordering = ["-id"]


class CompraCreateView(LoginRequiredMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = "compras/form.html"
    
    def get_success_url(self):
        return reverse_lazy("detalhes_compra", kwargs={"pk": self.object.pk})


class CompraUpdateView(LoginRequiredMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = "compras/form.html"
    
    def get_success_url(self):
        return reverse_lazy("detalhes_compra", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        compra = self.get_object()
        if not compra.is_editable:
            messages.error(request, "Não é possível editar uma compra que não está em rascunho.")
            return redirect("detalhes_compra", pk=compra.pk)
        return super().dispatch(request, *args, **kwargs)


class CompraDeleteView(LoginRequiredMixin, DeleteView):
    model = Compra
    template_name = "compras/excluir.html"
    success_url = reverse_lazy("listar_compras")

    def dispatch(self, request, *args, **kwargs):
        compra = self.get_object()
        if not compra.is_editable:
            messages.error(request, "Não é possível excluir uma compra que não está em rascunho.")
            return redirect("detalhes_compra", pk=compra.pk)
        return super().dispatch(request, *args, **kwargs)


class CompraDetailView(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = "compras/detalhe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compra = self.object
        
        # Pre-fetch grupos com os itens e produto
        context["grupos"] = compra.grupos.prefetch_related("itens__produto").select_related("fornecedor").all()
        
        if compra.is_editable:
            context["fornecedor_form"] = CompraFornecedorForm()
            context["item_form"] = ItemCompraForm()
            
        return context


@login_required
@require_POST
def adicionar_fornecedor(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    
    if not compra.is_editable:
        messages.error(request, "Não é possível alterar uma compra não rascunho.")
        return redirect("detalhes_compra", pk=pk)

    form = CompraFornecedorForm(request.POST)
    if form.is_valid():
        try:
            fornecedor = form.save(commit=False)
            fornecedor.compra = compra
            fornecedor.save()
            messages.success(request, "Fornecedor adicionado com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao adicionar fornecedor: Este fornecedor já pode estar na compra.")
    else:
        messages.error(request, "Erro no formulário de fornecedor.")
        
    return redirect("detalhes_compra", pk=pk)


@login_required
@require_POST
def remover_fornecedor(request, compra_pk, grupo_pk):
    grupo = get_object_or_404(CompraFornecedor, pk=grupo_pk, compra_id=compra_pk)
    
    if not grupo.compra.is_editable:
        messages.error(request, "Não é possível alterar uma compra não rascunho.")
    else:
        grupo.delete()
        messages.success(request, "Fornecedor removido com sucesso.")
        
    return redirect("detalhes_compra", pk=compra_pk)


@login_required
@require_POST
def adicionar_item(request, compra_pk, grupo_pk):
    grupo = get_object_or_404(CompraFornecedor, pk=grupo_pk, compra_id=compra_pk)
    
    if not grupo.compra.is_editable:
        messages.error(request, "Não é possível alterar itens em compra não rascunho.")
        return redirect("detalhes_compra", pk=compra_pk)

    form = ItemCompraForm(request.POST)
    form.instance.compra_fornecedor = grupo
    if form.is_valid():
        try:
            form.save()
            messages.success(request, "Item adicionado com sucesso.")
        except Exception as e:
            messages.error(request, "Erro ao adicionar item. Talvez o produto já esteja neste fornecedor.")
    else:
        messages.error(request, "Dados inválidos para o item.")
        
    return redirect("detalhes_compra", pk=compra_pk)


@login_required
@require_POST
def remover_item(request, compra_pk, item_pk):
    item = get_object_or_404(ItemCompra, pk=item_pk, compra_fornecedor__compra_id=compra_pk)
    
    if not item.compra_fornecedor.compra.is_editable:
        messages.error(request, "Não é possível remover itens em compra não rascunho.")
    else:
        item.delete()
        messages.success(request, "Item removido com sucesso.")
        
    return redirect("detalhes_compra", pk=compra_pk)


@login_required
@require_POST
def confirmar_compra_view(request, pk):
    try:
        confirmar_compra(pk)
        messages.success(request, "Compra confirmada com sucesso. Estoque atualizado.")
    except ValidationError as e:
        messages.error(request, e.message)
    except Compra.DoesNotExist:
        messages.error(request, "Compra não encontrada.")
    
    return redirect("detalhes_compra", pk=pk)


@login_required
@require_POST
def cancelar_compra_view(request, pk):
    try:
        cancelar_compra(pk)
        messages.success(request, "Compra cancelada com sucesso. Estoque atualizado.")
    except ValidationError as e:
        messages.error(request, e.message)
    except Compra.DoesNotExist:
        messages.error(request, "Compra não encontrada.")
    
    return redirect("detalhes_compra", pk=pk)
