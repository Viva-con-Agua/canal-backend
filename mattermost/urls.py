from django.urls import path
from . import views

urlpatterns = [
    path('user', views.createEmployee),
    path('user/exists', views.hasAccount),
    path('entity', views.addEntity),
    
]
