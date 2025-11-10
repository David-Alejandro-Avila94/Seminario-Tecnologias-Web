from django.urls import path
from . import views

urlpatterns = [
    path('', views.routine_list, name='routine_list'),
    path('create/', views.create_routine, name='create_routine'),
    path('<int:routine_id>/', views.routine_detail, name='routine_detail'),
    path('<int:routine_id>/add_day/', views.add_day, name='add_day'),
    path('day/<int:day_id>/add_exercise/', views.add_exercise, name='add_exercise'),
    path('exercise/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),

]
