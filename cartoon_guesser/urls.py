from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
]