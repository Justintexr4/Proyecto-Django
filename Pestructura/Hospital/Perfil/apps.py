# usuarios/apps.py

from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    name = 'Perfil'

    def ready(self):
        import Perfil.signals  # Importa las señales al iniciar la aplicación
