from django.db import models
from django.contrib.auth.models import User

class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Day(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='days')
    name = models.CharField(max_length=50)  # e.g., "Day 1", "Leg Day", etc.

    def __str__(self):
        return f"{self.name} - {self.routine.name}"

class Exercise(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='exercises')
    exercise_id = models.CharField(max_length=100)  # ID from ExerciseDB
    name = models.CharField(max_length=200)
    target = models.CharField(max_length=100, blank=True)
    gif_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
