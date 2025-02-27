from django.contrib import admin
from .models import CartoonSuggestion
from .models import CartoonCharacter

admin.site.register(CartoonCharacter)

@admin.register(CartoonSuggestion)
class CartoonSuggestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'submitted_at', 'submitter_ip') 
    list_filter = ('submitted_at',)  
    search_fields = ('name', 'description')  
    ordering = ('-submitted_at',)  