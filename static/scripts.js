function createRaindrop() {
    const raindrop = document.createElement('div');
    raindrop.className = 'raindrop';
    raindrop.style.left = Math.random() < 0.5 ? `${Math.random() * 20}%` : `${80 + Math.random() * 20}%`;
    raindrop.style.animationDuration = `${2 + Math.random() * 1.5}s`;
    document.querySelector('.raindrop-wrapper')?.appendChild(raindrop);
    setTimeout(() => raindrop.remove(), 4000);
}
setInterval(createRaindrop, 150);

function toggleNav() {
    document.querySelector('.navbar')?.classList.toggle('active');
}

function toggleAccountDropdown() {
    document.getElementById('account-dropdown')?.classList.toggle('active');
}

function handleModeClick(event, url) {
    if (event.button === 1) window.open(url, '_blank');
    else if (event.button === 0) window.location.href = url;
}

function playSound(id) {
    document.getElementById(id)?.play().catch(error => console.log(`${id} error:`, error));
}

document.addEventListener('click', (event) => {
    const accountContainer = document.querySelector('.account-container');
    const dropdown = document.getElementById('account-dropdown');
    if (accountContainer && dropdown && !accountContainer.contains(event.target) && dropdown.classList.contains('active')) {
        dropdown.classList.remove('active');
    }
});

function setupAutocomplete(inputId, data, callback) {
    const input = document.getElementById(inputId);
    if (!input) {
        console.error(`Input element with ID ${inputId} not found`);
        return;
    }
    const list = document.getElementById(`${inputId}-autocomplete-list`) || document.createElement('div');
    list.id = `${inputId}-autocomplete-list`;
    list.className = 'autocomplete-list';
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(list);
    let selectedIndex = -1;

    if (!data || !Array.isArray(data)) {
        console.error(`Autocomplete data for ${inputId} is invalid or empty`, data);
        return;
    }

    input.addEventListener('input', () => {
        const value = input.value.toLowerCase().trim();
        list.innerHTML = '';
        selectedIndex = -1;
        if (!value) return list.style.display = 'none';

        const matches = data.filter(item => item.name.toLowerCase().includes(value));
        matches.forEach((match, i) => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.innerHTML = `<img src="${match.image_url || 'https://via.placeholder.com/20'}" alt="${match.name}"> ${match.name}`;
            item.addEventListener('click', () => {
                input.value = match.name;
                list.style.display = 'none';
                if (callback) callback();
            });
            list.appendChild(item);
        });
        list.style.display = matches.length ? 'block' : 'none';
    });

    input.addEventListener('keydown', (e) => {
        const items = list.querySelectorAll('.autocomplete-item');
        if (!items.length) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
            updateSelection(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, -1);
            updateSelection(items);
        } else if (e.key === 'Enter' && selectedIndex >= 0) {
            e.preventDefault();
            input.value = items[selectedIndex].textContent.trim();
            list.style.display = 'none';
            if (callback) callback();
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (callback) callback();
        }
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !list.contains(e.target)) {
            list.style.display = 'none';
        }
    });

    function updateSelection(items) {
        items.forEach((item, i) => {
            item.classList.toggle('selected', i === selectedIndex);
            if (i === selectedIndex) {
                item.scrollIntoView({ block: 'nearest' });
                input.value = item.textContent.trim();
            }
        });
    }
}

// Global timer logic
const timerDisplay = document.getElementById('timer');
function updateTimer() {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
    tomorrow.setUTCHours(0, 0, 0, 0);
    const timeLeftMs = tomorrow - now;
    const hours = Math.floor(timeLeftMs / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeftMs % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeftMs % (1000 * 60)) / 1000);
    timerDisplay.textContent = `Next Daily Character: ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
document.addEventListener('DOMContentLoaded', () => {
    updateTimer();
    setInterval(updateTimer, 1000);
});

// Game logic functions
function submitGuess() {
    const guess = document.getElementById('guess-input')?.value.trim();
    if (!guess || (window.mode === 'daily' && window.guessCount >= 15)) return;

    console.log('Submitting guess:', guess);
    fetch('/guess/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '{{ csrf_token }}' },
        body: `guess=${encodeURIComponent(guess)}&mode=${window.mode}`
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        console.log('Guess response:', data);
        if (data.redirect) return window.location.href = data.redirect;
        if (data.error) return alert(data.error);

        window.guessCount = data.guess_count;
        window.guessCounter.textContent = `Guesses: ${window.guessCount}${window.mode === 'daily' ? '/15' : ''}`;
        updateKnownResults(data);
        updateHintButton();

        if (data.correct) {
            setTimeout(() => playSound('win-sound'), 100);
            if (window.mode === 'unlimited') {
                window.guessesContainer.innerHTML = '';
                window.guessCount = 0;
                window.hintUsed = false;
                window.guessCounter.textContent = 'Guesses: 0';
                window.knownValues = { name: '?', network: '?', show: '?', is_main: '?', release_year: '?', still_airing: '?', gender: '?', image: '?' };
                updateKnownResults({});
            }
        } else if (window.mode === 'daily' && window.guessCount >= 15) {
            setTimeout(() => playSound('lose-sound'), 100);
        }
        document.getElementById('guess-input').value = '';
    })
    .catch(error => console.error('Guess error:', error));
}

function updateKnownResults(data) {
    if (data.correct) {
        window.knownValues = {
            name: data.name,
            network: data.network_value,
            show: data.show_value,
            is_main: data.is_main ? 'Main' : 'Side',
            release_year: data.year_value,
            still_airing: data.still_airing ? 'Yes' : 'No',
            gender: data.gender_value,
            image: data.image_url || '?'
        };
    } else if (data.hint) {
        window.knownValues[data.hint.field] = data.hint.value;
    } else {
        if (data.network && !data.network_partial) window.knownValues.network = data.network_value;
        if (data.show) window.knownValues.show = data.show_value;
        if (data.main_correct) window.knownValues.is_main = data.is_main ? 'Main' : 'Side';
        if (data.release_year) window.knownValues.release_year = data.year_value;
        if (data.airing_correct) window.knownValues.still_airing = data.still_airing ? 'Yes' : 'No';
        if (data.gender) window.knownValues.gender = data.gender_value;
    }
    window.knownResults.innerHTML = `
        <div class="cell">${window.knownValues.image !== '?' ? `<img src="${window.knownValues.image}" alt="Character" style="max-width: 80px;">` : '?'}</div>
        <div class="cell ${window.knownValues.name !== '?' ? 'correct' : ''}"><span class="icon">👤</span>${window.knownValues.name}</div>
        <div class="cell ${window.knownValues.network !== '?' ? 'correct' : ''}"><span class="icon">📺</span>${window.knownValues.network}</div>
        <div class="cell ${window.knownValues.show !== '?' ? 'correct' : ''}"><span class="icon">🎬</span>${window.knownValues.show}</div>
        <div class="cell ${window.knownValues.is_main !== '?' ? 'correct' : ''}"><span class="icon">⭐</span>${window.knownValues.is_main}</div>
        <div class="cell ${window.knownValues.release_year !== '?' ? 'correct' : ''}"><span class="icon">📅</span>${window.knownValues.release_year}</div>
        <div class="cell ${window.knownValues.still_airing !== '?' ? 'correct' : ''}"><span class="icon">⏳</span>${window.knownValues.still_airing}</div>
        <div class="cell ${window.knownValues.gender !== '?' ? 'correct' : ''}"><span class="icon">🚻</span>${window.knownValues.gender}</div>
    `;

    if (!data.correct && !data.hint) {
        const row = document.createElement('div');
        row.className = 'grid';
        let yearIndicator = data.release_year ? '' : (data.year_value < data.daily_year ? ' ↑' : ' ↓');
        row.innerHTML = `
            <div class="cell"><img src="${data.image_url || 'https://via.placeholder.com/80'}" alt="${data.name}"></div>
            <div class="cell ${data.correct ? 'correct' : 'wrong'}"><span class="icon">👤</span>${data.name}</div>
            <div class="cell ${data.network ? 'correct' : (data.network_partial ? 'partial' : 'wrong')}"><span class="icon">📺</span>${data.network_value}</div>
            <div class="cell ${data.show ? 'correct' : 'wrong'}"><span class="icon">🎬</span>${data.show_value}</div>
            <div class="cell ${data.main_correct ? 'correct' : 'wrong'}"><span class="icon">⭐</span>${data.is_main ? 'Main' : 'Side'}</div>
            <div class="cell ${data.release_year ? 'correct' : (data.year_within_3 ? 'partial' : 'wrong')}"><span class="icon">📅</span>${data.year_value}${yearIndicator}</div>
            <div class="cell ${data.airing_correct ? 'correct' : 'wrong'}"><span class="icon">⏳</span>${data.still_airing ? 'Yes' : 'No'}</div>
            <div class="cell ${data.gender ? 'correct' : 'wrong'}"><span class="icon">🚻</span>${data.gender_value}</div>
        `;
        window.guessesContainer.insertBefore(row, window.guessesContainer.firstChild);
        row.querySelectorAll('.cell').forEach((cell, i) => setTimeout(() => cell.classList.add('reveal'), i * 200));
    }
}

function updateHintButton() {
    if (window.hintButton) window.hintButton.disabled = window.guessCount < 5 || window.hintUsed || (window.mode === 'daily' && window.guessCount >= 15);
}

function requestHint() {
    if (window.guessCount < 3 || window.hintUsed || (window.mode === 'daily' && window.guessCount >= 15)) return;
    fetch('/hint/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '{{ csrf_token }}' },
        body: `mode=${window.mode}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) return alert(data.error);
        window.hintUsed = true;
        updateKnownResults(data);
        updateHintButton();
    })
    .catch(error => console.error('Hint error:', error));
}

function giveUp() {
    playSound('lose-sound');
    window.location.href = `/lose/?mode=${window.mode}&gave_up=true`;
}