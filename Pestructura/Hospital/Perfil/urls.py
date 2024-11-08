from django.urls import path
from . import views
import resource

urlpatterns = [
  path('', views.home, name='home'),
  path('admin_login/', views.login_view, name='index'),
  path('logout/', views.logout_view, name='logout_view'),



]