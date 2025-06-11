from django.urls import path
from . import views

urlpatterns = [
    path('tryon/', views.tryon_api, name='tryon_api'),
]