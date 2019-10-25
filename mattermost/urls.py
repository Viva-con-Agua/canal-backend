from django.urls import path
from . import views

urlpatterns = [
    path('user', views.createUser),
    path('user/exists', views.hasAccount),
    
]
