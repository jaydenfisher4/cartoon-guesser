from django.contrib import admin
from .models import CartoonCharacter, CartoonSuggestion
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')

# Unregister the default User admin and register with custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)