from django.forms import ModelForm, TextInput, EmailInput, Select, CheckboxInput, Textarea, URLInput
from .models import Fornecedor

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 "
    "placeholder-gray-400 shadow-sm transition focus:border-gray-900 "
    "focus:outline-none focus:ring-2 focus:ring-gray-900/20"
)

CHECKBOX_CLASS = (
    "h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900 focus:ring-offset-2 transition cursor-pointer"
)


class FornecedorForm(ModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"
        widgets = {
            "nome": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Razão Social ou Nome do fornecedor"}),
            "cnpj": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "00.000.000/0000-00", "id": "id_cnpj"}),
            "categoria": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Categoria Ex: Eletrônicos"}),
            
            "telefone": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "(11) 99999-9999", "id": "id_telefone"}),
            "email": EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "email@fornecedor.com"}),
            "site": URLInput(attrs={"class": INPUT_CLASS, "placeholder": "https://www.site.com"}),
            "nome_representante": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Vendedor / Contato Comercial"}),

            "cep": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "00000-000", "id": "id_cep"}),
            "endereco": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Rua/Avenida"}),
            "numero": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Número"}),
            "complemento": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Complemento"}),
            "bairro": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Bairro"}),
            "cidade": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Cidade"}),
            "estado": Select(attrs={"class": INPUT_CLASS}),

            "banco": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Ex: Itaú, Nubank"}),
            "agencia": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "0000", "id": "id_agencia", "maxlength": "4"}),
            "conta": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "00000-0", "id": "id_conta"}),
            "chave_pix": TextInput(attrs={"class": INPUT_CLASS, "placeholder": "CNPJ, E-mail ou Celular"}),

            "is_active": CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
            "observacoes": Textarea(attrs={"class": INPUT_CLASS, "rows": 3, "placeholder": "Anotações adicionais, prazos ou regras comerciais"}),
        }
