# game/admin.py
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Show, CartoonCharacter, CartoonSuggestion, UserPreference
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'release_year', 'still_airing')
    search_fields = ('name', 'network')
    list_filter = ('still_airing',)  # Filter shows by still_airing

class ImageRestrictedFilter(SimpleListFilter):
    title = 'Image Status'
    parameter_name = 'image_restricted'

    def lookups(self, request, model_admin):
        return (
            ('restricted', 'Restricted Only'),
            ('unrestricted', 'Unrestricted Only'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'restricted':
            return queryset.filter(image_restricted=True)
        if self.value() == 'unrestricted':
            return queryset.filter(image_restricted=False)
        return queryset


class CartoonCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'get_network', 'get_release_year', 'get_still_airing', 'gender', 'is_main', 'image_restricted')
    list_filter = ('show', 'is_main', 'show__still_airing', 'show__release_year', ImageRestrictedFilter)
    search_fields = ('name', 'show__name', 'show__network')
    fields = ('name', 'show', 'gender', 'image_url', 'is_main', 'image_restricted')  # Fields for editing
    raw_id_fields = ('show',)  # Keep raw_id_fields for adding shows via popup

    # Custom methods to display Show fields in list_display
    def get_network(self, obj):
        return obj.show.network
    get_network.short_description = 'Network'

    def get_release_year(self, obj):
        return obj.show.release_year
    get_release_year.short_description = 'Release Year'

    def get_still_airing(self, obj):
        return obj.show.still_airing
    get_still_airing.short_description = 'Still Airing'

# Register models with admin
admin.site.register(Show, ShowAdmin)
admin.site.register(CartoonCharacter, CartoonCharacterAdmin)
admin.site.register(CartoonSuggestion)
admin.site.register(UserPreference)