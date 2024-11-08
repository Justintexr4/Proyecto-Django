from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_uso', 'En Uso'),
        ('mantenimiento', 'En Mantenimiento')
    ]

    RESOURCE_TYPES = [
        ('equipo_medico', 'Equipo Médico'),
        ('cama', 'Cama'),
        ('ventilador', 'Ventilador'),
        ('monitor', 'Monitor'),
        ('otro', 'Otro')
    ]

    name = models.CharField(max_length=100)
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        default='otro'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponible'
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):  # Cambiado de _str_ a __str__
        return f"{self.name} ({self.get_resource_type_display()})"


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    medical_record = models.CharField(max_length=50, unique=True)

    def __str__(self):  # Cambiado de _str_ a __str__
        return self.name


class ResourceAssignment(models.Model):
    PRIORITY_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('emergencia', 'Emergencia')
    ]

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    assignment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # Cambiado de _str_ a __str__
        return f"Asignación de {self.resource} a {self.patient}"


class ResourceOperationLog(models.Model):
    OPERATION_TYPES = [
        ('creación', 'Creación'),
        ('asignación', 'Asignación'),
        ('liberación', 'Liberación'),
        ('modificación', 'Modificación')
    ]

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # Cambiado de _str_ a __str__
        return f"{self.get_operation_type_display()} - {self.resource} por {self.user}"



