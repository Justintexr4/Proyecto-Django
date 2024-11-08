from django import forms
from .models import Resource, Patient, ResourceAssignment

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'resource_type', 'status', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class ResourceAssignForm(forms.ModelForm):
    class Meta:
        model = ResourceAssignment
        fields = ['resource', 'patient', 'priority']
        widgets = {
            'resource': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar recursos disponibles
        self.fields['resource'].queryset = Resource.objects.filter(status='disponible')