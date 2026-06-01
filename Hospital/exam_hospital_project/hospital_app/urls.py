from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:doctor_id>', views.doctor_detail, name='doctor_detail'),
]