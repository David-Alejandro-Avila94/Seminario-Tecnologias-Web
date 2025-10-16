from django.urls import path
from . import views
""" esto lo cree yo """
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]   