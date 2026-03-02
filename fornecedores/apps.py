from django.apps import AppConfig


class FornecedoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Python import path for the app
    name = 'fornecedores'
    # Keep the original app label so existing migrations still work
    label = 'forncedores'
