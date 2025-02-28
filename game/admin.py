# game/admin.py
from django.contrib import admin
from .models import Show, CartoonCharacter, CartoonSuggestion, UserPreference

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CartoonCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'network', 'release_year', 'still_airing')
    list_filter = ('show', 'still_airing', 'release_year')
    search_fields = ('name', 'network')
    # Add raw_id_fields to allow adding new shows via a popup
    raw_id_fields = ('show',)
    # Optional: If you want autocompletion instead of raw ID
    # autocomplete_fields = ('show',)

# Optional: If using autocomplete_fields, uncomment and configure search
# admin.site.register(Show, ShowAdmin, search_fields=['name'])

admin.site.register(Show, ShowAdmin)
admin.site.register(CartoonCharacter, CartoonCharacterAdmin)
admin.site.register(CartoonSuggestion)
admin.site.register(UserPreference)