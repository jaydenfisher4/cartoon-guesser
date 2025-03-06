from .models import CartoonCharacter
import logging

logger = logging.getLogger(__name__)

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
    all_characters_data = [{'name': char.name, 'image_url': char.image_url} for char in all_chars]
    logger.info(f"Context processor - Number of characters: {len(all_chars)}")
    logger.info(f"Context processor - Sample characters: {all_characters_data[:5]}")
    return {
        'all_characters': all_characters_data
    }