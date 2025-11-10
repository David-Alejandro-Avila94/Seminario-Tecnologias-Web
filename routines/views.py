from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Routine, Day, Exercise
import requests

API_BASE = "https://exercisedb.dev/api/v1/exercises"

@login_required
def routine_list(request):
    routines = Routine.objects.filter(user=request.user)
    return render(request, 'routines/routine_list.html', {'routines': routines})

@login_required
def create_routine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Routine.objects.create(user=request.user, name=name)
        return redirect('routine_list')
    return render(request, 'routines/create_routine.html')

@login_required
def routine_detail(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id, user=request.user)
    days = routine.days.all().prefetch_related('exercises')
    return render(request, 'routines/routine_detail.html', {
        'routine': routine,
        'days': days
    })

@login_required
def add_day(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        Day.objects.create(routine=routine, name=name)
        return redirect('routine_detail', routine_id=routine.id)
    return render(request, 'routines/add_day.html', {'routine': routine})

@login_required
def add_exercise(request, day_id):
    day = get_object_or_404(Day, id=day_id, routine__user=request.user)

    if request.method == 'POST':
        # Agregar ejercicio seleccionado
        exercise_id = request.POST.get('exercise_id')
        if exercise_id and exercise_id != 'None':
            Exercise.objects.create(
                day=day,
                exercise_id=exercise_id,
                name=request.POST.get('name'),
                target=request.POST.get('target'),
                gif_url=request.POST.get('gif_url')
            )
            return redirect('routine_detail', routine_id=day.routine.id)

        # Buscar ejercicios
        query = request.POST.get('query')
        if query:
            url = f"https://www.exercisedb.dev/api/v1/exercises/search?q={query}"
            response = requests.get(url)

            try:
                data = response.json()
            except ValueError:
                print("⚠️ La API no devolvió JSON válido:", response.text)
                data = {}

            print("DEBUG: API response type:", type(data))
            print("DEBUG: Keys:", data.keys() if isinstance(data, dict) else "No keys")

            results = []

            # ✅ Extraer lista real de ejercicios
            exercises = data.get("data", []) if isinstance(data, dict) else []

            for ex in exercises:
                if isinstance(ex, dict):
                    results.append({
                        "id": ex.get("exerciseId"),
                        "name": ex.get("name"),
                        "bodyPart": ", ".join(ex.get("bodyParts", [])),
                        "equipment": ", ".join(ex.get("equipments", [])),
                        "target": ", ".join(ex.get("targetMuscles", [])),
                        "gifUrl": ex.get("gifUrl"),
                    })

            return render(request, 'routines/add_exercise.html', {
                'day': day,
                'results': results,
                'query': query
            })

    return render(request, 'routines/add_exercise.html', {'day': day})


@login_required
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id, day__routine__user=request.user)
    routine_id = exercise.day.routine.id
    exercise.delete()
    return redirect('routine_detail', routine_id=routine_id)
