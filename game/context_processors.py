from .models import CartoonCharacter

def all_characters(request):
    if request.user.is_authenticated:
        try:
            prefs = request.user.userpreference
            excluded_shows = prefs.excluded_shows.all()
            excluded_chars = prefs.excluded_characters.all()
        except AttributeError:
            excluded_shows = []
            excluded_chars = []
    else:
        excluded_shows = []
        excluded_chars = []

    all_chars = CartoonCharacter.objects.select_related('show').exclude(
        show__in=excluded_shows
    ).exclude(
        id__in=excluded_chars
    ).exclude(
        image_restricted=True
    )
    return {
        'all_characters': [{'name': char.name, 'image_url': char.image_url} for char in all_chars]
    }