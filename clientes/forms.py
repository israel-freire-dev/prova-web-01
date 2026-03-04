from django.forms import EmailInput, ModelForm, TextInput

from .models import Cliente

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email"]
        widgets = {
            "nome": TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "Nome do cliente"}
            ),
            "email": EmailInput(
                attrs={"class": INPUT_CLASS, "placeholder": "email@exemplo.com"}
            ),
        }