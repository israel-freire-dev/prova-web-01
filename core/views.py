from django.views.generic import TemplateView
from django.db.models import F
from clientes.models import Cliente
from produtos.models import Produto
from fornecedores.models import Fornecedor
from compras.models import Compra

class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Clientes
        context['total_clientes'] = Cliente.objects.count()
        context['clientes_ativos'] = Cliente.objects.filter(ativo=True).count()
        
        # Produtos
        context['total_produtos'] = Produto.objects.count()
        context['produtos_ativos'] = Produto.objects.filter(ativo=True).count()
        context['produtos_baixo_estoque'] = Produto.objects.filter(quantidade__lte=F('estoque_minimo'), ativo=True).count()
        
        # Fornecedores
        context['total_fornecedores'] = Fornecedor.objects.count()
        context['fornecedores_ativos'] = Fornecedor.objects.filter(is_active=True).count()
        
        # Compras
        context['total_compras'] = Compra.objects.count()
        context['compras_rascunho'] = Compra.objects.filter(status=Compra.Status.RASCUNHO).count()
        context['compras_confirmadas'] = Compra.objects.filter(status=Compra.Status.CONFIRMADA).count()
        context['compras_canceladas'] = Compra.objects.filter(status=Compra.Status.CANCELADA).count()
        
        return context
