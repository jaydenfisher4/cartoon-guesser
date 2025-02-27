from django.contrib import admin
from .game.models import CartoonSuggestion

@admin.register(CartoonSuggestion)
class CartoonSuggestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'submitted_at', 'submitter_ip') 
    list_filter = ('submitted_at',)  
    search_fields = ('name', 'description')  
    ordering = ('-submitted_at',)  