from django.forms import DateInput, ModelForm, NumberInput, Select

from .models import Compra, ItemCompra

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)


class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ["fornecedor", "data"]
        widgets = {
            "fornecedor": Select(attrs={"class": INPUT_CLASS}),
            "data": DateInput(
                attrs={"class": INPUT_CLASS, "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se for editar, não permite mudar o fornecedor
        if self.instance and self.instance.pk:
            self.fields['fornecedor'].disabled = True


class ItemCompraForm(ModelForm):
    class Meta:
        model = ItemCompra
        fields = ["produto", "quantidade", "preco_unitario"]
        widgets = {
            "produto": Select(attrs={"class": INPUT_CLASS}),
            "quantidade": NumberInput(
                attrs={"class": INPUT_CLASS, "min": "1"}
            ),
            "preco_unitario": NumberInput(
                attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0.01"}
            ),
        }
