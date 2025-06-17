from django.apps import AppConfig

class ChamadosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chamados'

    # Adicione este método para registrar os sinais
    def ready(self):
        import chamados.signals