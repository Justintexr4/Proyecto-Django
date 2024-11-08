from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.resource_list, name='resource_list'),
    path('create/', views.resource_create, name='resource_create'),
    path('assign/', views.resource_assign, name='resource_assign'),
    path('release/<int:resource_id>/', views.resource_release, name='resource_release'),
    path('dashboard/', views.dashboard, name='dashboard'),

]