from django.shortcuts import render
from django.http import JsonResponse
from .models import CartoonCharacter
from datetime import date
import hashlib
import random

def get_daily_character():
    characters = CartoonCharacter.objects.all()
    if not characters:
        return None
    today = date.today().isoformat()
    index = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(characters)
    return characters[index]

def get_random_character(exclude_ids=None):
    characters = CartoonCharacter.objects.exclude(id__in=exclude_ids or [])
    if not characters:
        return None
    return random.choice(characters)

def index(request):
    daily_character = get_daily_character()
    all_characters = CartoonCharacter.objects.all()
    guesses = request.session.get('guesses-daily', [])
    all_characters_data = [char.name for char in all_characters]
    
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
        current_character = get_random_character(guessed_ids)
        if current_character:
            request.session['current_character_id-unlimited'] = current_character.id
    
    current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
    all_characters = CartoonCharacter.objects.all()
    all_characters_data = [char.name for char in all_characters]
    
    context = {
        'character': current_character,
        'guesses': guesses,
        'all_characters': all_characters_data,
        'mode': 'unlimited'
    }
    return render(request, 'game/index.html', context)

def characters_list(request):
    all_characters = CartoonCharacter.objects.all().order_by('name')
    context = {
        'characters': all_characters
    }
    return render(request, 'game/characters.html', context)

def guess(request):
    if request.method == 'POST':
        mode = request.POST.get('mode', 'daily')
        guess_name = request.POST.get('guess', '').strip()
        
        if mode == 'daily':
            current_character = get_daily_character()
            guesses_key = 'guesses-daily'
            guessed_ids_key = None
        else:  # unlimited
            current_character_id = request.session.get('current_character_id-unlimited')
            current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
            guesses_key = 'guesses-unlimited'
            guessed_ids_key = 'guessed_ids-unlimited'
            guessed_ids = request.session.get(guessed_ids_key, [])
        
        guesses = request.session.get(guesses_key, [])
        
        try:
            guessed_char = CartoonCharacter.objects.get(name__iexact=guess_name)
            network_correct = guessed_char.network == current_character.network
            network_partial = not network_correct and (
                guessed_char.network in current_character.network or
                current_character.network in guessed_char.network
            )
            main_correct = guessed_char.is_main == current_character.is_main
            airing_correct = guessed_char.still_airing == current_character.still_airing
            result = {
                'name': guessed_char.name,
                'network': network_correct,
                'network_value': guessed_char.network,
                'network_partial': network_partial,
                'show': guessed_char.show == current_character.show,
                'show_value': guessed_char.show,
                'is_main': guessed_char.is_main,
                'main_correct': main_correct,
                'release_year': guessed_char.release_year == current_character.release_year,
                'year_value': guessed_char.release_year,
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
        daily_character = get_daily_character()
    else:  # unlimited
        current_character_id = request.session.get('current_character_id-unlimited')
        daily_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        request.session['guesses-unlimited'] = []
        guessed_ids = request.session.get('guessed_ids-unlimited', [])
        new_character = get_random_character(guessed_ids)
        if new_character:
            request.session['current_character_id-unlimited'] = new_character.id
    
    context = {
        'character': daily_character,
        'mode': mode
    }
    return render(request, 'game/win.html', context)

def lose(request):
    mode = request.GET.get('mode', 'daily')
    if mode == 'daily':
        daily_character = get_daily_character()
    else:  # unlimited
        current_character_id = request.session.get('current_character_id-unlimited')
        daily_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        request.session['guesses-unlimited'] = []
        guessed_ids = request.session.get('guessed_ids-unlimited', [])
        new_character = get_random_character(guessed_ids)
        if new_character:
            request.session['current_character_id-unlimited'] = new_character.id
    
    context = {
        'character': daily_character,
        'mode': mode
    }
    return render(request, 'game/lose.html', context)