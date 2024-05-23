from django.db import models

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=50)
    task = models.CharField(max_length=250)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_action = models.CharField(max_length=250, blank=True)

    def __str__(self): #en lugar de regresare un objeto, da un texto del registro
        return f"{self.name} | limite -> {self.deadline}"
    