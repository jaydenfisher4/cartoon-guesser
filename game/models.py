from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    network = models.CharField(max_length=50, default='Unknown')  # Temporary default
    release_year = models.IntegerField(default=2000)              # Temporary default
    still_airing = models.BooleanField(default=False)             # Temporary default

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
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitter_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    excluded_shows = models.ManyToManyField(Show, blank=True)
    excluded_characters = models.ManyToManyField(CartoonCharacter, blank=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"