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

from .forms import CompraForm, ItemCompraForm
from .models import Compra, ItemCompra
from .serializers import CompraSerializer
from .services import cancelar_compra, confirmar_compra, confirmar_entrega


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


@api_view(["POST"])
def post_confirmar_entrega(request, compra_id: int):
    try:
        compra = confirmar_entrega(compra_id)
    except Compra.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    return Response(CompraSerializer(compra).data)


@api_view(["GET"])
def get_compra(request, compra_id: int):
    try:
        compra = Compra.objects.get(pk=compra_id)
    except Compra.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(CompraSerializer(compra).data)


from django.http import JsonResponse
from produtos.models import Produto

@login_required
def get_produtos_fornecedor_api(request, fornecedor_id):
    # Endpoint simplificado que retorna JSON com id, nome de produtos de um fornecedor
    produtos = Produto.objects.filter(fornecedor_id=fornecedor_id, ativo=True)
    dados = [{"id": p.id, "nome": p.nome} for p in produtos]
    return JsonResponse(dados, safe=False)



# --- Template Views ---

class CompraListView(LoginRequiredMixin, ListView):
    model = Compra
    template_name = "compras/lista.html"
    context_object_name = "compras"
    ordering = ["-id"]

    def get_queryset(self):
        # Otimiza a listagem carregando previamente Fornecedor e Produtos
        return super().get_queryset().select_related("fornecedor").prefetch_related(
            "itens__produto"
        )


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
            messages.error(request, "Não é possível editar uma ordem de compra que não está em rascunho.")
            return redirect("detalhes_compra", pk=compra.pk)
        return super().dispatch(request, *args, **kwargs)


class CompraDeleteView(LoginRequiredMixin, DeleteView):
    model = Compra
    template_name = "compras/excluir.html"
    success_url = reverse_lazy("listar_compras")

    def dispatch(self, request, *args, **kwargs):
        compra = self.get_object()
        if not compra.is_editable:
            messages.error(request, "Não é possível excluir uma ordem de compra que não está em rascunho.")
            return redirect("detalhes_compra", pk=compra.pk)
        return super().dispatch(request, *args, **kwargs)


class CompraDetailView(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = "compras/detalhe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compra = self.object
        
        # Pre-fetch itens e produto
        context["itens"] = compra.itens.select_related("produto").all()
        
        if compra.is_editable:
            context["item_form"] = ItemCompraForm()
            # O form de itens não deveria carregar todos, mas sim os específicos do fornecedor
            # Faremos isso via JS no template, mas inicializamos vazio
            if context["item_form"].fields.get("produto"):
                from produtos.models import Produto
                context["item_form"].fields["produto"].queryset = Produto.objects.filter(fornecedor=compra.fornecedor, ativo=True)
            
        return context


@login_required
@require_POST
def adicionar_item(request, compra_pk):
    compra = get_object_or_404(Compra, pk=compra_pk)
    
    if not compra.is_editable:
        messages.error(request, "Não é possível alterar itens em ordem não-rascunho.")
        return redirect("detalhes_compra", pk=compra_pk)

    form = ItemCompraForm(request.POST)
    form.instance.compra = compra
    if form.is_valid():
        try:
            form.save()
            messages.success(request, "Item adicionado com sucesso.")
        except Exception as e:
            messages.error(request, "Erro ao adicionar item. Talvez o produto já esteja na ordem.")
    else:
        messages.error(request, "Dados inválidos para o item.")
        
    return redirect("detalhes_compra", pk=compra_pk)


@login_required
@require_POST
def remover_item(request, compra_pk, item_pk):
    item = get_object_or_404(ItemCompra, pk=item_pk, compra_id=compra_pk)
    
    if not item.compra.is_editable:
        messages.error(request, "Não é possível remover itens em ordem não-rascunho.")
    else:
        item.delete()
        messages.success(request, "Item removido com sucesso.")
        
    return redirect("detalhes_compra", pk=compra_pk)


@login_required
@require_POST
def confirmar_compra_view(request, pk):
    try:
        confirmar_compra(pk)
        messages.success(request, "Ordem de compra confirmada com sucesso.")
    except ValidationError as e:
        messages.error(request, e.message)
    except Compra.DoesNotExist:
        messages.error(request, "Ordem não encontrada.")
    
    return redirect("detalhes_compra", pk=pk)


@login_required
@require_POST
def confirmar_entrega_view(request, pk):
    try:
        confirmar_entrega(pk)
        messages.success(request, "Entrega confirmada com sucesso. Estoque atualizado.")
    except ValidationError as e:
        messages.error(request, e.message)
    except Compra.DoesNotExist:
        messages.error(request, "Ordem não encontrada.")
    
    return redirect("detalhes_compra", pk=pk)


@login_required
@require_POST
def cancelar_compra_view(request, pk):
    try:
        cancelar_compra(pk)
        messages.success(request, "Ordem de compra cancelada com sucesso.")
    except ValidationError as e:
        messages.error(request, e.message)
    except Compra.DoesNotExist:
        messages.error(request, "Ordem não encontrada.")
    
    return redirect("detalhes_compra", pk=pk)

