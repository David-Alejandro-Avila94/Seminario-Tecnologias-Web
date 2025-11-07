from django.apps import AppConfig
from django.shortcuts import render


class GymConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gym'


def home(request):
    return render(request, 'gym/index.html') 

