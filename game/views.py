from django.shortcuts import render, redirect, get_object_or_404 
from django.http import JsonResponse
from .models import CartoonCharacter, UserPreference, Show, DailyGameHistory, FriendRequest, Friendship
from datetime import date, datetime, timedelta
import hashlib
import random
import logging
from .forms import CartoonSuggestionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Count, Min, Q

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_exclusions(request):
    if request.user.is_authenticated:
        try:
            prefs = UserPreference.objects.get(user=request.user)
            return prefs.excluded_shows.all(), prefs.excluded_characters.all()
        except UserPreference.DoesNotExist:
            return Show.objects.none(), CartoonCharacter.objects.none()
    return Show.objects.none(), CartoonCharacter.objects.none()

def get_daily_character(request, excluded_shows=None, excluded_chars=None):
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
        daily_character = characters.order_by('id')[index]
        logger.debug(f"Daily character selected: {daily_character.name}")
        return daily_character
    except IndexError:
        return None

def get_random_character(request, exclude_ids=None, excluded_shows=None, excluded_chars=None):
    if excluded_shows is None or excluded_chars is None:
        excluded_shows, excluded_chars = get_user_exclusions(request)

    characters = CartoonCharacter.objects.select_related('show').exclude(
        show__in=excluded_shows
    ).exclude(
        id__in=excluded_chars
    ).exclude(
        id__in=exclude_ids or []
    )

    character = characters.order_by('?').first()
    if character:
        logger.debug(f"Random character selected: {character.name}")
    return character

def index(request):
    if request.GET.get('reset'):  # For testing
        request.session.flush()
        return redirect('index')

    today = date.today().isoformat()
    session_date = request.session.get('daily_character_date')
    daily_character_id = request.session.get('daily_character_id')
    game_over = request.session.get('daily_game_over', False)

    if session_date == today and game_over:
        guesses = request.session.get('guesses-daily', [])
        try:
            daily_character = CartoonCharacter.objects.get(id=daily_character_id)
            return redirect('win' if guesses and guesses[-1] == daily_character.name else 'lose')
        except CartoonCharacter.DoesNotExist:
            pass  # Proceed to reset if character not found

    if session_date != today or not daily_character_id or not game_over:
        excluded_shows, excluded_chars = get_user_exclusions(request)
        daily_character = get_daily_character(request, excluded_shows, excluded_chars)
        if daily_character:
            request.session['daily_character_id'] = daily_character.id
            request.session['daily_character_date'] = today
            request.session['daily_game_over'] = False
        else:
            daily_character = None

    excluded_shows, excluded_chars = get_user_exclusions(request)
    all_characters = CartoonCharacter.objects.select_related('show').exclude(
        show__in=excluded_shows
    ).exclude(
        id__in=excluded_chars
    ).exclude(
        image_restricted=True
    )
    all_characters_data = [{'name': char.name, 'image_url': char.image_url} for char in all_characters]
    guesses = request.session.get('guesses-daily', [])
    request.session['last_mode'] = 'daily'
    request.session.setdefault('hint_used-daily', False)
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

    excluded_shows, excluded_chars = get_user_exclusions(request)
    if not current_character_id or current_character_id not in guessed_ids:
        current_character = get_random_character(request, guessed_ids, excluded_shows, excluded_chars)
        if current_character:
            request.session['current_character_id-unlimited'] = current_character.id
        else:
            current_character = None
    else:
        current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None

    all_characters = CartoonCharacter.objects.select_related('show').exclude(
        show__in=excluded_shows
    ).exclude(
        id__in=excluded_chars
    ).exclude(
        image_restricted=True
    )
    all_characters_data = [{'name': char.name, 'image_url': char.image_url} for char in all_characters]
    request.session['last_mode'] = 'unlimited'
    request.session.setdefault('hint_used-unlimited', False)

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

    excluded_shows, excluded_chars = get_user_exclusions(request)
    excluded_show_ids = set(excluded_shows.values_list('id', flat=True))
    excluded_char_ids = set(excluded_chars.values_list('id', flat=True))

    context = {
        'characters': [
            {
                'name': char.name,
                'show': char.show.name,
                'network': char.network,
                'release_year': char.release_year,
                'still_airing': char.still_airing,
                'is_main': char.is_main,
                'gender': char.gender,
                'image_url': char.image_url,
                'is_excluded': char.id in excluded_char_ids or char.show.id in excluded_show_ids
            } for char in all_characters
        ],
        'shows': shows,
        'single_networks': single_networks,
        'years': years,
        'last_mode': last_mode
    }
    return render(request, 'game/characters.html', context)

def guess(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    mode = request.POST.get('mode', 'daily')
    guess_name = request.POST.get('guess', '').strip()

    if mode == 'daily':
        today = date.today().isoformat()
        session_date = request.session.get('daily_character_date')
        if session_date != today or request.session.get('daily_game_over', False):
            return JsonResponse({'error': 'Daily game is over for today'}, status=400)
        current_character = get_daily_character(request)
        guesses_key = 'guesses-daily'
        hint_key = 'hint_used-daily'
        guessed_ids_key = None
    else:
        current_character_id = request.session.get('current_character_id-unlimited')
        current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        guesses_key = 'guesses-unlimited'
        hint_key = 'hint_used-unlimited'
        guessed_ids_key = 'guessed_ids-unlimited'
        guessed_ids = request.session.get(guessed_ids_key, [])

    guesses = request.session.get(guesses_key, [])

    try:
        guessed_char = CartoonCharacter.objects.get(name__iexact=guess_name)
        guess_networks = set(guessed_char.network.split(', '))
        target_networks = set(current_character.network.split(', '))
        network_exact = (guess_networks == target_networks)
        network_partial = bool(guess_networks & target_networks) and not network_exact
        main_match = guessed_char.is_main == current_character.is_main
        airing_match = guessed_char.still_airing == current_character.still_airing
        year_match = guessed_char.release_year == current_character.release_year
        year_within_3 = not year_match and abs(guessed_char.release_year - current_character.release_year) <= 3
        gender_match = guessed_char.gender == current_character.gender
        show_match = guessed_char.show == current_character.show

        result = {
            'name': guessed_char.name,
            'network': network_exact,
            'network_value': guessed_char.network,
            'network_partial': network_partial,
            'show': show_match,
            'show_value': guessed_char.show.name if guessed_char.show else None,
            'is_main': guessed_char.is_main,
            'main_correct': main_match,
            'release_year': year_match,
            'year_value': guessed_char.release_year,
            'year_within_3': year_within_3,
            'daily_year': current_character.release_year,
            'still_airing': guessed_char.still_airing,
            'airing_correct': airing_match,
            'gender': gender_match,
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
            elif mode == 'daily' and (result['correct'] or len(guesses) >= 15):
                request.session['daily_game_over'] = True
                DailyGameHistory.objects.create(
                    user=request.user,
                    date=date.today(),
                    character_name=current_character.name,
                    won=result['correct'],
                    guess_count=len(guesses)
                )

        logger.info(f"Guess response: {json.dumps(result)}")
        if result['correct'] or (mode == 'daily' and len(guesses) >= 15):
            return JsonResponse({'redirect': f"/{'win' if result['correct'] else 'lose'}/?mode={mode}"})
        return JsonResponse(result)
    except CartoonCharacter.DoesNotExist:
        return JsonResponse({'error': 'Character not found'}, status=404)
    
def hint(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    mode = request.POST.get('mode', 'daily')
    hint_key = 'hint_used-' + mode
    guesses_key = 'guesses-' + mode

    if request.session.get(hint_key, False):
        return JsonResponse({'error': 'Hint already used'}, status=400)

    guesses = request.session.get(guesses_key, [])
    if len(guesses) < 3:
        return JsonResponse({'error': 'Not enough guesses for a hint'}, status=400)

    if mode == 'daily':
        today = date.today().isoformat()
        if request.session.get('daily_character_date') != today or request.session.get('daily_game_over', False):
            return JsonResponse({'error': 'Daily game is over'}, status=400)
        current_character = get_daily_character(request)
    else:
        current_character_id = request.session.get('current_character_id-unlimited')
        current_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None

    if not current_character:
        return JsonResponse({'error': 'No character available'}, status=500)

    known = set()
    for guess_name in guesses:
        try:
            guessed_char = CartoonCharacter.objects.get(name__iexact=guess_name)
            if guessed_char.network == current_character.network:
                known.add('network')
            if guessed_char.show == current_character.show:
                known.add('show')
            if guessed_char.is_main == current_character.is_main:
                known.add('is_main')
            if guessed_char.release_year == current_character.release_year:
                known.add('release_year')
            if guessed_char.still_airing == current_character.still_airing:
                known.add('still_airing')
            if guessed_char.gender == current_character.gender:
                known.add('gender')
        except CartoonCharacter.DoesNotExist:
            continue

    hint_options = ['network', 'is_main', 'release_year', 'still_airing', 'gender']
    unknown_options = [field for field in hint_options if field not in known]

    if unknown_options:
        hint_field = random.choice(unknown_options)
    elif 'show' not in known:
        hint_field = 'show'
    elif 'image' not in known:
        hint_field = 'image'
    else:
        return JsonResponse({'error': 'No new hints available'}, status=400)

    request.session[hint_key] = True

    if hint_field == 'image':
        value = current_character.image_url
    elif hint_field == 'show':
        value = current_character.show.name
    elif hint_field == 'is_main':
        value = 'Main' if current_character.is_main else 'Side'
    elif hint_field == 'release_year':
        value = str(current_character.release_year)
    elif hint_field == 'network':
        value = current_character.network
    elif hint_field == 'gender':
        value = current_character.gender
    elif hint_field == 'still_airing':
        value = 'Yes' if current_character.still_airing else 'No'

    logger.info(f"Hint response: {json.dumps({'hint': {'field': hint_field, 'value': value}})}")
    return JsonResponse({'hint': {'field': hint_field, 'value': value}})

def win(request):
    mode = request.GET.get('mode', 'daily')
    today = date.today().isoformat()
    if mode == 'daily':
        daily_character = get_daily_character(request)
        if request.session.get('daily_character_date') != today or not request.session.get('daily_game_over', False):
            return redirect('index')
    else:
        current_character_id = request.session.get('current_character_id-unlimited')
        daily_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        request.session['guesses-unlimited'] = []
        request.session['hint_used-unlimited'] = False
        guessed_ids = request.session.get('guessed_ids-unlimited', [])
        new_character = get_random_character(request, guessed_ids)
        if new_character:
            request.session['current_character_id-unlimited'] = new_character.id
        else:
            del request.session['current_character_id-unlimited']

    context = {
        'character': daily_character,
        'mode': mode,
    }
    return render(request, 'game/win.html', context)

def lose(request):
    mode = request.GET.get('mode', 'daily')
    gave_up = request.GET.get('gave_up', 'false') == 'true'
    today = date.today().isoformat()
    if mode == 'daily':
        daily_character = get_daily_character(request)
        if request.session.get('daily_character_date') != today or not request.session.get('daily_game_over', False):
            return redirect('index')
    else:
        current_character_id = request.session.get('current_character_id-unlimited')
        daily_character = CartoonCharacter.objects.get(id=current_character_id) if current_character_id else None
        request.session['guesses-unlimited'] = []
        request.session['hint_used-unlimited'] = False
        guessed_ids = request.session.get('guessed_ids-unlimited', [])
        new_character = get_random_character(request, guessed_ids)
        if new_character:
            request.session['current_character_id-unlimited'] = new_character.id
        else:
            del request.session['current_character_id-unlimited']

    context = {
        'character': daily_character,
        'mode': mode,
        'gave_up': gave_up
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
def exclusions(request):
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
    return render(request, 'game/exclusions.html', context)

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

@login_required
def set_profile_picture(request):
    if request.method == 'POST':
        image_url = request.POST.get('image_url')
        if image_url:
            preference, created = UserPreference.objects.get_or_create(user=request.user)
            preference.profile_picture = image_url
            preference.save()
            return JsonResponse({'success': True, 'url': image_url})
        return JsonResponse({'success': False, 'error': 'No image data'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

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

def about(request):
    return render(request, 'game/about.html')

def recent_changes(request):
    return render(request, 'game/recent_changes.html')

@csrf_exempt
def report_image_restriction(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    name = request.POST.get('name')
    restricted = request.POST.get('restricted') == 'true'

    try:
        character = CartoonCharacter.objects.get(name=name)
        if character.image_restricted != restricted:
            character.image_restricted = restricted
            character.save()
            logger.info(f"Updated {name} image_restricted to {restricted}")
        return JsonResponse({'success': True})
    except CartoonCharacter.DoesNotExist:
        logger.error(f"Character {name} not found")
        return JsonResponse({'success': False, 'error': 'Character not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating {name}: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@login_required
def profile(request, username=None):
    if username:
        try:
            profile_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('profile')
    else:
        profile_user = request.user

    prefs, _ = UserPreference.objects.get_or_create(user=profile_user)
    
    # Daily streak
    history = DailyGameHistory.objects.filter(user=profile_user).order_by('-date')
    daily_streak = 0
    current_date = date.today()
    for entry in history:
        if entry.date == current_date and entry.won:
            daily_streak += 1
            current_date -= timedelta(days=1)
        elif entry.date > current_date:
            continue
        else:
            break
    
    # Best score
    best_score = DailyGameHistory.objects.filter(user=profile_user, won=True).aggregate(Min('guess_count'))['guess_count__min']
    
    # Total wins
    total_daily_wins = DailyGameHistory.objects.filter(user=profile_user, won=True).count()
    total_unlimited_wins = len(request.session.get('guessed_ids-unlimited', [])) if profile_user == request.user else 0
    
    # Favorite character
    favorite_character = DailyGameHistory.objects.filter(user=profile_user, won=True).values('character_name').annotate(count=Count('character_name')).order_by('-count').first()
    favorite_character_name = favorite_character['character_name'] if favorite_character else None

    # Friend status
    is_friend = Friendship.objects.filter(
        Q(user1=request.user, user2=profile_user) | Q(user1=profile_user, user2=request.user)
    ).exists()
    has_sent_request = FriendRequest.objects.filter(from_user=request.user, to_user=profile_user, accepted=False).exists()
    received_request = FriendRequest.objects.filter(from_user=profile_user, to_user=request.user, accepted=False).first()
    has_received_request = received_request is not None

    # Fetch friends with their profile pictures
    friendships = Friendship.objects.filter(
        Q(user1=profile_user) | Q(user2=profile_user)
    ).select_related('user1__userpreference', 'user2__userpreference')
    friend_list = []
    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == profile_user else friendship.user1
        friend_list.append({
            'username': friend.username,
            'profile_picture': friend.userpreference.profile_picture if hasattr(friend, 'userpreference') else None
        })

    context = {
        'profile_user': profile_user,
        'daily_streak': daily_streak,
        'best_score': best_score,
        'total_daily_wins': total_daily_wins,
        'total_unlimited_wins': total_unlimited_wins if profile_user == request.user else None,
        'favorite_character': favorite_character_name,
        'daily_history': history[:10],
        'is_friend': is_friend,
        'has_sent_request': has_sent_request,
        'has_received_request': has_received_request,
        'received_request': received_request,
        'friend_list': friend_list,  # Updated to include profile_picture
        'is_own_profile': profile_user == request.user,
    }
    return render(request, 'game/profile.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'game/search_users.html', context)

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if to_user == request.user:
        return redirect('profile')
    if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('profile', username=username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if not friend_request.accepted:
        friend_request.accepted = True
        friend_request.save()
        Friendship.objects.create(user1=request.user, user2=friend_request.from_user)
    return redirect('profile')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    return redirect('profile')