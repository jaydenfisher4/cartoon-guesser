from django.contrib import admin
from .models import CartoonCharacter, CartoonSuggestion

class CartoonCharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'network', 'release_year']  # Removed 'show' for now

admin.site.register(CartoonCharacter, CartoonCharacterAdmin)
admin.site.register(CartoonSuggestion)