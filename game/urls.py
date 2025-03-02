from django.urls import path
from game import views

urlpatterns = [
    path('', views.index, name='index'),
    path('unlimited/', views.unlimited, name='unlimited'),
    path('characters/', views.characters_list, name='characters'),
    path('guess/', views.guess, name='guess'),
    path('hint/', views.hint, name='hint'),
    path('win/', views.win, name='win'),
    path('lose/', views.lose, name='lose'),
    path('suggest/', views.submit_suggestion, name='suggest'),
    path('exclusions/', views.exclusions, name='exclusions'),
    path('get_characters/<int:show_id>/', views.get_characters, name='get_characters'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('recent-changes/', views.recent_changes, name='recent_changes'),
     path('set-profile-picture/', views.set_profile_picture, name='set_profile_picture'),
]