from django.db import models
from django.contrib.auth.models import User

class CartoonCharacter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    show = models.CharField(max_length=100)
    network = models.CharField(max_length=50)
    is_main = models.BooleanField(default=True)
    release_year = models.IntegerField()
    still_airing = models.BooleanField(default=False)
    gender = models.CharField(max_length=20)
    image_url = models.URLField(max_length=999, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.show})"  # Display the character's name in the admin

class CartoonSuggestion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitter_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    excluded_shows = models.TextField(blank=True)  # Comma-separated show names
    excluded_characters = models.TextField(blank=True)  # Comma-separated character names

    def get_excluded_shows_list(self):
        return [show.strip() for show in self.excluded_shows.split(',') if show.strip()]

    def get_excluded_characters_list(self):
        return [char.strip() for char in self.excluded_characters.split(',') if char.strip()]