from django.db import models

class CartoonCharacter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    show = models.CharField(max_length=100)
    network = models.CharField(max_length=50)
    is_main = models.BooleanField(default=True)
    release_year = models.IntegerField()
    still_airing = models.BooleanField(default=False)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.name