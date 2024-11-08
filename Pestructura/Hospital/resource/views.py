from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    Resource,
    ResourceOperationLog,
    ResourceAssignment,
    Patient
)
from .forms import (
    ResourceForm,
    ResourceAssignForm
)
@login_required
def resource_list(request):
    """
    Vista para listar todos los recursos
    """
    resources = Resource.objects.all()
    return render(request, 'resource_list.html', {'resources': resources})


@login_required
def resource_create(request):
    """
    Vista para crear un nuevo recurso
    """
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save()

            # Registrar operación en log
            ResourceOperationLog.objects.create(
                resource=resource,
                user=request.user,
                operation_type='creación'
            )

            messages.success(request, 'Recurso creado exitosamente')
            return redirect('resource_list')
    else:
        form = ResourceForm()

    return render(request, 'resource_form.html', {'form': form})


@login_required
def resource_assign(request):
    """
    Vista para asignar un recurso
    """
    if request.method == 'POST':
        form = ResourceAssignForm(request.POST)
        if form.is_valid():
            try:
                # Obtener datos del formulario
                resource = form.cleaned_data['resource']
                patient = form.cleaned_data['patient']
                priority = form.cleaned_data['priority']
                assignment_date = form.cleaned_data['assignment_date']

                # Crear asignación de recurso
                ResourceAssignment.objects.create(
                    resource=resource,
                    patient=patient,
                    priority=priority,
                    assignment_date=assignment_date
                )

                # Actualizar estado del recurso
                resource.status = 'en_uso'
                resource.save()

                # Registrar operación en log
                ResourceOperationLog.objects.create(
                    resource=resource,
                    user=request.user,
                    operation_type='asignación'
                )

                messages.success(request, 'Recurso asignado exitosamente')
                return redirect('resource_list')

            except Exception as e:
                messages.error(request, f'Error al asignar recurso: {str(e)}')
    else:
        form = ResourceAssignForm()

    return render(request, 'resource_assign.html', {'form': form})


@login_required
def resource_release(request, resource_id):
    """
    Vista para liberar un recurso
    """
    resource = get_object_or_404(Resource, id=resource_id)

    try:
        # Liberar recurso
        resource.status = 'disponible'
        resource.save()

        # Registrar operación en log
        ResourceOperationLog.objects.create(
            resource=resource,
            user=request.user,
            operation_type='liberación'
        )

        messages.success(request, 'Recurso liberado exitosamente')
    except Exception as e:
        messages.error(request, f'Error al liberar recurso: {str(e)}')

    return redirect('resource_list')


def dashboard(request):
    """
    Vista para el panel de control de recursos
    """
    # Estadísticas de recursos
    total_resources = Resource.objects.count()
    available_resources = Resource.objects.filter(status='disponible').count()
    used_resources = Resource.objects.filter(status='en_uso').count()
    maintenance_resources = Resource.objects.filter(status='mantenimiento').count()

    # Logs recientes
    recent_logs = ResourceOperationLog.objects.order_by('-timestamp')[:10]

    context = {
        'total_resources': total_resources,
        'available_resources': available_resources,
        'used_resources': used_resources,
        'maintenance_resources': maintenance_resources,
        'recent_logs': recent_logs
    }

    return render(request, 'dashboard.html', context)


class ResourceCreateView(CreateView):
    """
    Vista basada en clase para crear recursos
    """
    model = Resource
    form_class = ResourceForm
    template_name = 'resource_form.html'
    success_url = reverse_lazy('resource_list')

    def form_valid(self, form):
        """
        Método para manejar el formulario válido
        """
        response = super().form_valid(form)

        # Registrar operación en log
        ResourceOperationLog.objects.create(
            resource=self.object,
            user=self.request.user,
            operation_type='creación'
        )

        return response