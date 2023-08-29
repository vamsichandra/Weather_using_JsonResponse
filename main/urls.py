from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('API/', views.get_weather, name='API'),

]
