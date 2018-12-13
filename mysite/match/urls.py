from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('matches/', views.match, name='matches'),
    path('filtering/', views.filtering, name='filtering'),
]
