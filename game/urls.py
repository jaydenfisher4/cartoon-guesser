from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('unlimited/', views.unlimited, name='unlimited'),
    path('guess/', views.guess, name='guess'),
    path('win/', views.win, name='win'),
    path('lose/', views.lose, name='lose'),
    path('characters/', views.characters_list, name='characters_list'),
    path('suggest/', views.submit_suggestion, name='suggest'),
    path('register/', views.register, name='register'),
    path('preferences/', views.preferences, name='preferences'),
]