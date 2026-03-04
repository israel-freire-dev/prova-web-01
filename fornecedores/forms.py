from django.forms import BooleanField, CheckboxInput, EmailInput, ModelForm, TextInput

from .models import Fornecedor


INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 "
    "focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)


class FornecedorForm(ModelForm):
    is_active = BooleanField(
        required=False,
        widget=CheckboxInput(
            attrs={
                "class": (
                    "h-4 w-4 rounded border-gray-300 text-gray-900 "
                    "focus:ring-2 focus:ring-gray-900/20"
                )
            }
        ),
        label="Fornecedor ativo",
    )

    class Meta:
        model = Fornecedor
        fields = ("nome", "telefone", "email", "categoria", "cidade", "estado", "cnpj", "is_active")
        widgets = {
            "nome": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "Nome do fornecedor"}
            ),
            "telefone": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "(11) 99999-9999"}
            ),
            "email": EmailInput(
                attrs={"class": INPUT_CLASS, "placeholder": "email@fornecedor.com"}
            ),
            "categoria": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "Categoria do fornecedor"}
            ),
            "cidade": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "Cidade"}
            ),
            "estado": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "Estado"}
            ),
            "cnpj": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "00.000.000/0000-00"}
            ),
        }

