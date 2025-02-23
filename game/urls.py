from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Daily mode
    path('unlimited/', views.unlimited, name='unlimited'),  # Unlimited mode
    path('guess/', views.guess, name='guess'),
    path('win/', views.win, name='win'),
    path('lose/', views.lose, name='lose'),
]