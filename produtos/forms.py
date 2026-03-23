from django.forms import ModelForm, TextInput, NumberInput, DateInput
from .models import Produto


INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 "
    "focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "preco", "quantidade", "data_validade"]
        widgets = {
            "nome": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "Nome do produto"}
            ),
            "preco": NumberInput(
                attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}
            ),
            "quantidade": NumberInput(
                attrs={"class": INPUT_CLASS, "min": "0"}
            ),
            "data_validade": DateInput(
                attrs={"class": INPUT_CLASS, "type": "date"}
            ),
        }
