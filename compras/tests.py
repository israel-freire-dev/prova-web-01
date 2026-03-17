from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from fornecedores.models import Fornecedor
from produtos.models import Produto

from .models import Compra, CompraFornecedor, ItemCompra
from .services import cancelar_compra, confirmar_compra


class CompraEstoqueFlowTests(TestCase):
    def setUp(self) -> None:
        self.fornecedor1 = Fornecedor.objects.create(nome="Fornecedor A")
        self.fornecedor2 = Fornecedor.objects.create(nome="Fornecedor B")

        self.produto1 = Produto.objects.create(
            nome="Produto 1",
            preco=10.0,
            quantidade=5,
            data_validade=date.today() + timedelta(days=365),
        )
        self.produto2 = Produto.objects.create(
            nome="Produto 2",
            preco=20.0,
            quantidade=2,
            data_validade=date.today() + timedelta(days=365),
        )

    def test_confirmar_compra_multifornecedor_soma_estoque(self):
        compra = Compra.objects.create()

        grupo1 = CompraFornecedor.objects.create(compra=compra, fornecedor=self.fornecedor1)
        grupo2 = CompraFornecedor.objects.create(compra=compra, fornecedor=self.fornecedor2)

        ItemCompra.objects.create(
            compra_fornecedor=grupo1,
            produto=self.produto1,
            quantidade=3,
            preco_unitario=Decimal("9.90"),
        )
        ItemCompra.objects.create(
            compra_fornecedor=grupo2,
            produto=self.produto2,
            quantidade=4,
            preco_unitario=Decimal("19.90"),
        )

        confirmar_compra(compra.id)

        self.produto1.refresh_from_db()
        self.produto2.refresh_from_db()
        compra.refresh_from_db()

        self.assertEqual(compra.status, Compra.Status.CONFIRMADA)
        self.assertEqual(self.produto1.quantidade, 8)  # 5 + 3
        self.assertEqual(self.produto2.quantidade, 6)  # 2 + 4

    def test_cancelar_compra_confirmada_estorna_estoque(self):
        compra = Compra.objects.create()
        grupo = CompraFornecedor.objects.create(compra=compra, fornecedor=self.fornecedor1)
        ItemCompra.objects.create(
            compra_fornecedor=grupo,
            produto=self.produto1,
            quantidade=2,
            preco_unitario=Decimal("10.00"),
        )

        confirmar_compra(compra.id)
        cancelar_compra(compra.id)

        self.produto1.refresh_from_db()
        compra.refresh_from_db()

        self.assertEqual(compra.status, Compra.Status.CANCELADA)
        self.assertEqual(self.produto1.quantidade, 5)  # voltou ao original

    def test_confirmar_duas_vezes_falha(self):
        compra = Compra.objects.create()
        grupo = CompraFornecedor.objects.create(compra=compra, fornecedor=self.fornecedor1)
        ItemCompra.objects.create(
            compra_fornecedor=grupo,
            produto=self.produto1,
            quantidade=1,
            preco_unitario=Decimal("10.00"),
        )

        confirmar_compra(compra.id)

        with self.assertRaises(ValidationError):
            confirmar_compra(compra.id)

    def test_cancelar_rascunho_nao_mexe_no_estoque(self):
        compra = Compra.objects.create()
        grupo = CompraFornecedor.objects.create(compra=compra, fornecedor=self.fornecedor1)
        ItemCompra.objects.create(
            compra_fornecedor=grupo,
            produto=self.produto1,
            quantidade=2,
            preco_unitario=Decimal("10.00"),
        )

        cancelar_compra(compra.id)

        self.produto1.refresh_from_db()
        compra.refresh_from_db()
        self.assertEqual(compra.status, Compra.Status.CANCELADA)
        self.assertEqual(self.produto1.quantidade, 5)

    def test_nao_permite_alterar_itens_apos_confirmacao(self):
        compra = Compra.objects.create()
        grupo = CompraFornecedor.objects.create(compra=compra, fornecedor=self.fornecedor1)
        item = ItemCompra.objects.create(
            compra_fornecedor=grupo,
            produto=self.produto1,
            quantidade=1,
            preco_unitario=Decimal("10.00"),
        )

        confirmar_compra(compra.id)
        compra.refresh_from_db()

        item.quantidade = 2
        with self.assertRaises(ValidationError):
            item.full_clean()
