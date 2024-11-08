from django.contrib import admin

# Register your models here.
# usuarios/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Perfil

# Definir una clase en línea para Perfil
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

# Crear un UserAdmin personalizado
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

    # Mostrar el rol en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'mostrar_rol')
    list_select_related = ('perfil',)

    def mostrar_rol(self, instance):
        return instance.perfil.rol
    mostrar_rol.short_description = 'Rol del usuario'

# Desregistrar el modelo User original y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registrar el modelo Perfil, en caso de querer administrarlo por separado
admin.site.register(Perfil)
