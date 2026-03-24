from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import F
from django.contrib.auth.models import User
from clientes.models import Cliente
from produtos.models import Produto
from fornecedores.models import Fornecedor
from compras.models import Compra
from .forms import CustomUserCreationForm

class IndexView(LoginRequiredMixin, TemplateView):
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

class CadastroView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'core/cadastro.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
