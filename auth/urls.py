from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_pool),
    path('redirectUri/', views.redirect_uri),
]
