from django.urls import path
from profiles import views

urlpatterns = [
    # URL patterns for profile views
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]
