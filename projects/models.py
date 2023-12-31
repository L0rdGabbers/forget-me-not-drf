from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Model representing a project.

    A project is owned by a user and may have collaborators. It has a due date,
    title, summary, completion status, and an optional image.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    collaborators = models.ManyToManyField(
        User, related_name="projects_collaborated", blank=True)
    complete = models.BooleanField(blank=True, null=False, default=False)
    image = models.ImageField(
        upload_to='images/', default='../rjstswgoqpakct7vhsy7', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'ID# {self.id}: {self.title}'
