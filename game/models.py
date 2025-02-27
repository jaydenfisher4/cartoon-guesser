from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Show(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class CartoonCharacter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    network = models.CharField(max_length=50)
    is_main = models.BooleanField(default=True)
    release_year = models.IntegerField()
    still_airing = models.BooleanField(default=False)
    gender = models.CharField(max_length=20)
    image_url = models.URLField(max_length=999, blank=True, null=True)

class CartoonSuggestion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitter_ip = models.GenericIPAddressField(null=True, blank=True)
    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Old fields (keep temporarily)
    excluded_shows = models.TextField(blank=True, null=True)
    excluded_characters = models.TextField(blank=True, null=True)
    # New JSONFields
    excluded_shows_json = JSONField(default=list, blank=True)
    excluded_characters_json = JSONField(default=list, blank=True)