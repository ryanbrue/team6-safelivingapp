from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:ORI>/', views.getScorebyORI),
]