from django.urls import path
from game import views

urlpatterns = [
    path('', views.index, name='index'),
    path('unlimited/', views.unlimited, name='unlimited'),
    path('characters/', views.characters_list, name='characters'),
    path('guess/', views.guess, name='guess'),
    path('win/', views.win, name='win'),
    path('lose/', views.lose, name='lose'),
    path('suggest/', views.submit_suggestion, name='suggest'),
    path('preferences/', views.preferences, name='preferences'),
    path('get_characters/<int:show_id>/', views.get_characters, name='get_characters'),
    path('register/', views.register, name='register'),
    # Add login/logout URLs as needed
]