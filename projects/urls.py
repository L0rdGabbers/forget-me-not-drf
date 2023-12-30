from django.urls import path
from projects import views

urlpatterns = [
    # URL patterns for project views
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view())
]