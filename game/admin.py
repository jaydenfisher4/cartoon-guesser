from django.contrib import admin
from .models import CartoonCharacter, CartoonSuggestion

class CartoonCharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'show', 'network', 'release_year']

admin.site.register(CartoonCharacter, CartoonCharacterAdmin)
admin.site.register(CartoonSuggestion)