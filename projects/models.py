from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    collaborators = models.ManyToManyField(User, related_name="projects_collaborated", blank=True)
    complete = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='images/', default='../rjstswgoqpakct7vhsy7', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'