from django.forms import EmailInput, ModelForm, TextInput, Select, DateInput, CheckboxInput, Textarea

from .models import Cliente

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)

CHECKBOX_CLASS = (
    "h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900 focus:ring-offset-2 transition cursor-pointer"
)


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nome", "email", "cpf", "telefone", "data_nascimento",
            "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado",
            "ativo", "observacoes"
        ]
        widgets = {
            "nome": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Nome do cliente"}),
            "email": EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "email@exemplo.com"}),
            "cpf": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "000.000.000-00"}),
            "telefone": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "(00) 00000-0000"}),
            "data_nascimento": DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "cep": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "00000-000"}),
            "endereco": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Logradouro"}),
            "numero": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Número"}),
            "complemento": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Complemento"}),
            "bairro": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Bairro"}),
            "cidade": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Cidade"}),
            "estado": Select(attrs={"class": INPUT_CLASS}),
            "ativo": CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
            "observacoes": Textarea(attrs={"class": INPUT_CLASS, "rows": 3, "placeholder": "..."}),
        }