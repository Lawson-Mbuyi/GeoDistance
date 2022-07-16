from django.urls import path
from .views import distance_compute


urlpatterns = [
    path('', distance_compute)
 ]