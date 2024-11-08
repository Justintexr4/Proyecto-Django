from django.db import models

# Create your models here.


from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    ROLES = [
        ('enfermero', 'Enfermero'),
        ('doctor', 'Doctor'),
        ('administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"









