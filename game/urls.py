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
    path('report-image-restriction/', views.report_image_restriction, name='report_image_restriction'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('search-users/', views.search_users, name='search_users'),
    path('search-users-autocomplete/', views.search_users_autocomplete, name='search_users_autocomplete'),
    path('send-friend-request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]