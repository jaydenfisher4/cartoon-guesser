from django.contrib import admin
from .models import CartoonCharacter, CartoonSuggestion

@admin.register(CartoonSuggestion)
class CartoonSuggestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'submitted_at', 'submitter_ip')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'description')
    ordering = ('-submitted_at',)

@admin.register(CartoonCharacter)
class CartoonCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'network', 'release_year')  # Customize columns
    search_fields = ('name', 'show')  # Optional: add search
    list_filter = ('network', 'still_airing')  # Optional: add filters