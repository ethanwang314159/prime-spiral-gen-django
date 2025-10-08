from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('spiral/', views.spiral_image, name='spiral_image'),
    path('spiral/json/', views.spiral_settings_json, name='spiral_settings_json'),
]
