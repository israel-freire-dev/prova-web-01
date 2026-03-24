from django.forms import ModelForm, TextInput, NumberInput, DateInput, Select, CheckboxInput, Textarea
from .models import Produto

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 "
    "focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)

CHECKBOX_CLASS = (
    "h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900 focus:ring-offset-2 transition cursor-pointer"
)


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome", "descricao", "codigo", "categoria", "marca", "unidade_medida", "fornecedor",
            "preco_custo", "preco_venda", "quantidade", "estoque_minimo", "data_validade",
            "ativo", "observacoes"
        ]
        widgets = {
            "nome": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Nome do produto"}),
            "descricao": Textarea(attrs={"class": INPUT_CLASS, "rows": 3, "placeholder": "Descrição do produto..."}),
            "codigo": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "SKU / Código"}),
            "categoria": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Ex: Bebidas"}),
            "marca": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Ex: Coca-Cola"}),
            "unidade_medida": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Ex: UN, KG, LT"}),
            "fornecedor": Select(attrs={"class": INPUT_CLASS}),
            "preco_custo": NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "preco_venda": NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "quantidade": NumberInput(attrs={"class": INPUT_CLASS, "min": "0"}),
            "estoque_minimo": NumberInput(attrs={"class": INPUT_CLASS, "min": "0"}),
            "data_validade": DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "ativo": CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
            "observacoes": Textarea(attrs={"class": INPUT_CLASS, "rows": 3, "placeholder": "Observações..."}),
        }
