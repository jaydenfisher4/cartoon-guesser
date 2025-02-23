from django.shortcuts import render
from django.http import JsonResponse
from .models import CartoonCharacter
from datetime import date
import hashlib

def get_daily_character():
    characters = CartoonCharacter.objects.all()
    if not characters:
        return None
    today = date.today().isoformat()
    index = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(characters)
    return characters[index]

def index(request):
    daily_character = get_daily_character()
    all_characters = CartoonCharacter.objects.all()
    guesses = request.session.get('guesses', [])
    all_characters_data = [char.name for char in all_characters]
    
    context = {
        'character': daily_character,
        'guesses': guesses,
        'all_characters': all_characters_data
    }
    return render(request, 'game/index.html', context)

def guess(request):
    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session['guesses'] = []
            return JsonResponse({'status': 'reset'})
        
        guess_name = request.POST.get('guess', '').strip()
        daily_character = get_daily_character()
        guesses = request.session.get('guesses', [])
        
        try:
            guessed_char = CartoonCharacter.objects.get(name__iexact=guess_name)
            network_correct = guessed_char.network == daily_character.network
            network_partial = not network_correct and (
                guessed_char.network in daily_character.network or
                daily_character.network in guessed_char.network
            )
            result = {
                'name': guessed_char.name,
                'network': network_correct,
                'network_partial': network_partial,
                'show': guessed_char.show == daily_character.show,
                'is_main': guessed_char.is_main == daily_character.is_main,
                'release_year': guessed_char.release_year == daily_character.release_year,
                'guessed_year': guessed_char.release_year,
                'daily_year': daily_character.release_year,
                'still_airing': guessed_char.still_airing == daily_character.still_airing,
                'gender': guessed_char.gender == daily_character.gender,
                'correct': guessed_char.id == daily_character.id,
                'guess_count': len(guesses) + 1  # Send current guess count
            }
            if guess_name not in guesses:
                guesses.append(guess_name)
                request.session['guesses'] = guesses[:15]  # Increased to 15
            if result['correct']:
                return JsonResponse({'redirect': '/win/'})
            elif len(guesses) >= 15:
                return JsonResponse({'redirect': '/lose/'})
            return JsonResponse(result)
        except CartoonCharacter.DoesNotExist:
            return JsonResponse({'error': 'Character not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def win(request):
    daily_character = get_daily_character()
    context = {
        'character': daily_character
    }
    return render(request, 'game/win.html', context)

def lose(request):
    daily_character = get_daily_character()
    context = {
        'character': daily_character
    }
    return render(request, 'game/lose.html', context)