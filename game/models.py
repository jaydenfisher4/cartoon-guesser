# game/models.py
from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    network = models.CharField(max_length=50)
    release_year = models.IntegerField()
    still_airing = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CartoonCharacter(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=True)
    gender = models.CharField(max_length=20)
    image_url = models.URLField(max_length=999, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def network(self):
        return self.show.network

    @property
    def release_year(self):
        return self.show.release_year

    @property
    def still_airing(self):
        return self.show.still_airing

class CartoonSuggestion(models.Model):
    SUGGESTION_TYPES = [
        ('show', 'New Show'),
        ('character', 'Missing Character'),
        ('feedback', 'Site Feedback'),
    ]
    suggestion_type = models.CharField(max_length=10, choices=SUGGESTION_TYPES, default='show')
    show_name = models.CharField(max_length=100, blank=True)
    existing_show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True)
    character_name = models.CharField(max_length=100, blank=True)
    feedback = models.TextField(blank=True)
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitter_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        if self.suggestion_type == 'show':
            return self.show_name
        elif self.suggestion_type == 'character':
            return f"{self.character_name} ({self.existing_show})"
        return "Feedback"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    excluded_shows = models.ManyToManyField(Show, blank=True)
    excluded_characters = models.ManyToManyField(CartoonCharacter, blank=True)
    profile_picture = models.TextField(blank=True, null=True)  # Store base64 string

    def __str__(self):
        return f"Preferences for {self.user.username}"