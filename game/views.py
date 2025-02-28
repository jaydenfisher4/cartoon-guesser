from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CartoonCharacter, UserPreference, Show
from datetime import date
import hashlib
import random
import logging
from .forms import CartoonSuggestionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_exclusions(request):
    """Helper to get user's excluded shows and characters as QuerySets."""
    if request.user.is_authenticated:
        try:
            prefs = UserPreference.objects.get(user=request.user)
            return prefs.excluded_shows.all(), prefs.excluded_characters.all()
        except UserPreference.DoesNotExist:
            return Show.objects.none(), CartoonCharacter.objects.none()
    return Show.objects.none(), CartoonCharacter.objects.none()

def get_daily_character(request, excluded_shows=None, excluded_chars=None):
    """Get the daily character, filtered by user exclusions."""
    if excluded_shows is None or excluded_chars is None:
        excluded_shows, excluded_chars = get_user_exclusions(request)
    
    characters = CartoonCharacter.objects.select_related('show').exclude(
        show__in=excluded_shows
    ).exclude(
        id__in=excluded_chars
    )
    
    count = characters.count()
    if count == 0:
        return None
    
    today = date.today().isoformat()
    index = int(hashlib.md5(today.encode()).hexdigest(), 16) % count
    try:
        # Order consistently and use slicing (note: this may still hit performance with large offsets)
        daily_character = characters.order_by('id')[index]
        logger.debug(f"Daily character selected: {daily_character.name}")
        return daily_character
    except IndexError:
        return None

def get_random_character(request, exclude_ids=None, excluded_shows=None, excluded_chars=None):
    """Get a random character, filtered by exclusions."""
    if excluded_shows is None or excluded_chars is None:
        excluded_shows, excluded_chars = get_user_exclusions(request)
    
    characters = CartoonCharacter.objects.select_related('show').exclude(
        show__in=excluded_shows
    ).exclude(
        id__in=excluded_chars
    ).exclude(
        id__in=exclude_ids or []
    )
    
    # Use database random selection (Postgres ORDER BY RANDOM())
    character = characters.order_by('?').first()
    if character:
        logger.debug(f"Random character selected: {character.name}")
    return character

def index(request):
    today = date.today().isoformat()
    session_date = request.session.get('daily_character_date')
    daily_character_id = request.session.get('daily_character_id')
    
    if session_date == today and daily_character_id:
        try:
            daily_character = CartoonCharacter.objects.get(id=daily_character_id)
        except CartoonCharacter.DoesNotExist:
            daily_character = None
    else:
        excluded_shows, excluded_chars = get_user_exclusions(request)
        daily_character = get_daily_character(request, excluded_shows, excluded_chars)
        if daily_character:
            request.session['daily_character_id'] = daily_character.id
            request.session['daily_character_date'] = today
    
    all_characters = CartoonCharacter.objects.select_related('show').all()
    guesses = request.session.get('guesses-daily', [])
    all_characters_data = [char.name for char in all_characters]
    request.session['last_mode'] = 'daily'
    context = {
        'character': daily_character,
        'guesses': guesses,
        'all_characters': all_characters_data,
        'mode': 'daily'
    }
    return render(request, 'game/index.html', context)

def unlimited(request):
    guesses = request.session.get('guesses-unlimited', [])
    guessed_ids = request.session.get('guessed_ids-unlimited', [])
    current_character_id = request.session.get('current_character_id-unlimited')

    if not current_character_id or current_character_id not in guessed_ids:
        excluded_shows, excluded_chars = get_user_exclusions(request)
        current_character = get_random_character(request, guessed_ids, excluded_shows, excluded_chars)
        if current_character:
            request.session['current_character_id-unlimited'] = current_character.id
        else:
            current_character = None
    else:
        current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None

    all_characters = CartoonCharacter.objects.select_related('show').all()
    all_characters_data = [char.name for char in all_characters]
    request.session['last_mode'] = 'unlimited'

    context = {
        'character': current_character,
        'guesses': guesses,
        'all_characters': all_characters_data,
        'mode': 'unlimited'
    }
    return render(request, 'game/index.html', context)

def characters_list(request):
    all_characters = CartoonCharacter.objects.select_related('show').order_by('name')
    shows = sorted(set(char.show.name for char in all_characters))
    all_networks = set()
    for char in all_characters:
        networks = char.network.split(', ')
        all_networks.update(networks)
    single_networks = sorted(all_networks)
    years = sorted(set(char.release_year for char in all_characters))
    last_mode = request.session.get('last_mode', 'daily')

    context = {
        'characters': all_characters,
        'shows': shows,
        'single_networks': single_networks,
        'years': years,
        'last_mode': last_mode
    }
    return render(request, 'game/characters.html', context)

def guess(request):
    if request.method == 'POST':
        mode = request.POST.get('mode', 'daily')
        guess_name = request.POST.get('guess', '').strip()

        if mode == 'daily':
            current_character = get_daily_character(request)
            guesses_key = 'guesses-daily'
            guessed_ids_key = None
        else:
            current_character_id = request.session.get('current_character_id-unlimited')
            current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
            guesses_key = 'guesses-unlimited'
            guessed_ids_key = 'guessed_ids-unlimited'
            guessed_ids = request.session.get(guessed_ids_key, [])

        guesses = request.session.get(guesses_key, [])

        try:
            guessed_char = CartoonCharacter.objects.get(name__iexact=guess_name)
            guess_networks = set(guessed_char.network.split(', '))
            target_networks = set(current_character.network.split(', '))
            network_correct = guess_networks == target_networks
            network_partial = not network_correct and bool(guess_networks & target_networks)
            main_correct = guessed_char.is_main == current_character.is_main
            airing_correct = guessed_char.still_airing == current_character.still_airing
            year_correct = guessed_char.release_year == current_character.release_year
            year_within_3 = not year_correct and abs(guessed_char.release_year - current_character.release_year) <= 3
            result = {
                'name': guessed_char.name,
                'network': network_correct,
                'network_value': guessed_char.network,
                'network_partial': network_partial,
                'show': guessed_char.show == current_character.show,
                'show_value': guessed_char.show.name if guessed_char.show else None,
                'is_main': guessed_char.is_main,
                'main_correct': main_correct,
                'release_year': year_correct,
                'year_value': guessed_char.release_year,
                'year_within_3': year_within_3,
                'daily_year': current_character.release_year,
                'still_airing': guessed_char.still_airing,
                'airing_correct': airing_correct,
                'gender': guessed_char.gender == current_character.gender,
                'gender_value': guessed_char.gender,
                'image_url': guessed_char.image_url,
                'correct': guessed_char.id == current_character.id,
                'guess_count': len(guesses) + 1,
                'mode': mode,
                'current_character_id': current_character.id if mode == 'unlimited' else None
            }
            if guess_name not in guesses:
                guesses.append(guess_name)
                request.session[guesses_key] = guesses[:15]
                if mode == 'unlimited' and result['correct']:
                    guessed_ids.append(current_character.id)
                    request.session[guessed_ids_key] = guessed_ids

            if result['correct']:
                return JsonResponse({'redirect': '/win/?mode=' + mode})
            elif len(guesses) >= 15:
                return JsonResponse({'redirect': '/lose/?mode=' + mode})
            return JsonResponse(result)
        except CartoonCharacter.DoesNotExist:
            return JsonResponse({'error': 'Character not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def win(request):
    mode = request.GET.get('mode', 'daily')
    if mode == 'daily':
        daily_character = get_daily_character(request)
    else:
        current_character_id = request.session.get('current_character_id-unlimited')
        daily_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        request.session['guesses-unlimited'] = []
        guessed_ids = request.session.get('guessed_ids-unlimited', [])
        new_character = get_random_character(request, guessed_ids)
        if new_character:
            request.session['current_character_id-unlimited'] = new_character.id
        else:
            del request.session['current_character_id-unlimited']

    context = {
        'character': daily_character,
        'mode': mode
    }
    return render(request, 'game/win.html', context)

def lose(request):
    mode = request.GET.get('mode', 'daily')
    if mode == 'daily':
        daily_character = get_daily_character(request)
    else:
        current_character_id = request.session.get('current_character_id-unlimited')
        daily_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        request.session['guesses-unlimited'] = []
        guessed_ids = request.session.get('guessed_ids-unlimited', [])
        new_character = get_random_character(request, guessed_ids)
        if new_character:
            request.session['current_character_id-unlimited'] = new_character.id
        else:
            del request.session['current_character_id-unlimited']

    context = {
        'character': daily_character,
        'mode': mode
    }
    return render(request, 'game/lose.html', context)

def submit_suggestion(request):
    if request.method == 'POST':
        form = CartoonSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.submitter_ip = request.META.get('REMOTE_ADDR')
            suggestion.save()
            return redirect('index')
    else:
        form = CartoonSuggestionForm()
    return render(request, 'game/suggestion.html', {'form': form})

@login_required
def preferences(request):
    preferences, created = UserPreference.objects.get_or_create(user=request.user)
    all_shows = Show.objects.all()

    if request.method == 'POST':
        excluded_shows_ids = request.POST.getlist('excluded_shows')
        excluded_characters_ids = request.POST.getlist('excluded_characters')
        preferences.excluded_shows.set(excluded_shows_ids)
        preferences.excluded_characters.set(excluded_characters_ids)
        preferences.save()
        return redirect('index')

    context = {
        'preferences': preferences,
        'all_shows': all_shows,
    }
    return render(request, 'game/preferences.html', context)

@login_required
def get_characters(request, show_id):
    show = Show.objects.get(id=show_id)
    characters = show.cartooncharacter_set.all()
    prefs = UserPreference.objects.get(user=request.user)
    excluded_ids = set(prefs.excluded_characters.values_list('id', flat=True))
    characters_data = [
        {'id': char.id, 'name': char.name, 'excluded': char.id in excluded_ids}
        for char in characters
    ]
    return JsonResponse({'characters': characters_data})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            UserPreference.objects.create(user=user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})