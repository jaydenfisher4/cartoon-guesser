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
    if request.user.is_authenticated:
        try:
            prefs = UserPreference.objects.get(user=request.user)
            excluded_shows = [s.strip() for s in (prefs.excluded_shows or '').split(',') if s.strip()]
            excluded_chars = [c.strip() for c in (prefs.excluded_characters or '').split(',') if c.strip()]
            return excluded_shows, excluded_chars
        except UserPreference.DoesNotExist:
            return [], []
    return [], []

def get_daily_character(request):
    characters = CartoonCharacter.objects.all()
    if not characters:
        return None
    excluded_shows, excluded_chars = get_user_exclusions(request)
    available = [c for c in characters if c.show not in excluded_shows and c.name not in excluded_chars]
    if not available:
        return None
    today = date.today().isoformat()
    index = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(available)
    logger.debug(f"Daily character selected: {available[index].name}")
    return available[index]

def get_random_character(request, exclude_ids=None):
    characters = CartoonCharacter.objects.exclude(id__in=exclude_ids or [])
    excluded_shows, excluded_chars = get_user_exclusions(request)
    available = [c for c in characters if c.show not in excluded_shows and c.name not in excluded_chars]
    if not available:
        return None
    chosen = random.choice(available)
    logger.debug(f"Random character selected: {chosen.name}")
    return chosen

def index(request):
    daily_character = get_daily_character(request)
    all_characters = CartoonCharacter.objects.all()
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
        current_character = get_random_character(request, guessed_ids)
        if current_character:
            request.session['current_character_id-unlimited'] = current_character.id
    
    current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
    all_characters = CartoonCharacter.objects.all()
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
    all_characters = CartoonCharacter.objects.all().order_by('name')
    shows = sorted(set(char.show for char in all_characters))
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
                'show_value': guessed_char.show,
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
        # Get selected shows and characters as lists
        excluded_shows = request.POST.getlist('excluded_shows')
        excluded_characters = request.POST.getlist('excluded_characters')
        preferences.excluded_shows = excluded_shows
        preferences.excluded_characters = excluded_characters
        preferences.save()
        return redirect('index')

    context = {
        'preferences': preferences,
        'all_shows': all_shows,
    }
    return render(request, 'game/preferences.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            UserPreference.objects.create(user=user)  # Create empty preferences
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})