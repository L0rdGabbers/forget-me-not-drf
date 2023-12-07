from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

importance_choices = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('crucial', 'Crucial'),
    ]


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    collaborators = models.ManyToManyField(User, related_name="tasks_collaborated", blank=True)
    importance = models.CharField(
        max_length=32, choices=importance_choices, default='low'
    )
    complete = models.BooleanField(blank=True, null=False, default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'ID# {self.id}: {self.title}'
