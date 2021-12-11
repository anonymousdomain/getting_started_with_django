from django.urls import path

from . import views

app_name = 'pizzeria'

urlpatterns = [
    path('pizza', views.pizza, name='pizza')
]
