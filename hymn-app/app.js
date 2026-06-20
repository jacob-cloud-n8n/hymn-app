/**
 * Hymn App - 詩歌點播
 */

const CATEGORIES = ['大本詩歌', '新歌頌詠', '新詩', '補充本'];
const CAT_DISPLAY = { '大本詩歌': '詩歌', '新歌頌詠': '新歌', '新詩': '新詩', '補充本': '補充' };

let hymnsData = {};
let state = {
    category: '大本詩歌',
    input: '',
    queue: [],
    queueIndex: 0,
};

// ===== DATA LOADING =====
async function loadData() {
    try {
        const res = await fetch('data/hymns.json');
        hymnsData = await res.json();
        updatePreview();
    } catch (e) {
        console.error('Failed to load hymns:', e);
        alert('載入詩歌資料失敗，請確認 data/hymns.json 存在');
    }
}

// ===== HELPERS =====
function getSongs(cat) {
    return hymnsData[cat] || [];
}

function findSong(cat, id) {
    const songs = getSongs(cat);
    const cleanId = id.replace(/^附/, '');
    // Try exact match first
    let match = songs.find(s => s.id === id);
    if (match) return match;
    // Try padded matches
    if (cat === '補充本') {
        match = songs.find(s => s.id === cleanId.padStart(4, '0'));
    } else {
        match = songs.find(s => s.id === cleanId.padStart(3, '0'));
    }
    return match;
}

function formatId(cat, id) {
    if (cat === '補充本') return id.padStart(4, '0');
    return id.padStart(3, '0');
}

function formatKey(key) {
    if (!key) return '';
    // Convert "G 4/4" to "G 大調 4/4" roughly
    const m = key.match(/^([A-G][b#]?)\s+(\d\/\d)$/);
    if (m) {
        return `${m[1]} 大調 ${m[2]}`;
    }
    return key;
}

function formatLyrics(lyrics) {
    if (!lyrics || lyrics.length === 0) return '（暫無歌詞，僅有目錄）\n\n歡迎提供歌詞資料，或從詩歌本手動輸入。';
    const text = lyrics.join('\n');

    // Strategy: split by verse markers, keeping the marker with its content
    // Markers: 一) 二) 三) ... 十) 副)
    const markerPattern = /([一二三四五六七八九十]+\)|副\))/g;
    const parts = text.split(markerPattern).filter(p => p.trim());

    if (parts.length <= 1) {
        // No markers found, just return cleaned text with line breaks
        return text.replace(/\n+/g, '\n').trim();
    }

    // Reassemble: markers and their content
    const lines = [];
    for (let i = 0; i < parts.length; i++) {
        const part = parts[i].trim();
        if (part.match(/^[一二三四五六七八九十]+\)$/)) {
            // This is a marker, next part is its content
            lines.push(''); // blank line before verse
            if (i + 1 < parts.length) {
                lines.push(part + ' ' + parts[i + 1].trim());
                i++; // skip next since we consumed it
            } else {
                lines.push(part);
            }
        } else if (part === '副)') {
            lines.push('');
            if (i + 1 < parts.length) {
                lines.push('（副）' + parts[i + 1].trim());
                i++;
            } else {
                lines.push('（副）');
            }
        } else {
            lines.push(part);
        }
    }

    return lines.join('\n').replace(/\n+/g, '\n').trim();
}

// ===== UI UPDATES =====
function updatePreview() {
    const disp = document.getElementById('input-display');
    const preview = document.getElementById('preview-name');
    disp.textContent = state.input || '';

    if (state.input) {
        const song = findSong(state.category, state.input);
        preview.textContent = song ? song.title : '（無此編號）';
    } else {
        preview.textContent = '';
    }
}

function updateQueueBar() {
    const count = document.getElementById('queue-count');
    const catName = CAT_DISPLAY[state.category];
    count.textContent = `${catName} ${state.queue.length} 首`;
}

function switchTab(cat) {
    state.category = cat;
    state.input = '';
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.cat === cat);
    });
    updatePreview();
    updateQueueBar();
}

function showPage(name) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`page-${name}`).classList.add('active');
}

// ===== DIALPAD =====
function handleKey(key) {
    if (key === 'del') {
        state.input = state.input.slice(0, -1);
    } else if (key === '附') {
        if (!state.input.startsWith('附')) {
            state.input = '附' + state.input;
        }
    } else {
        state.input += key;
    }
    updatePreview();
}

function playCurrent() {
    if (!state.input) return;
    const song = findSong(state.category, state.input);
    if (!song) {
        alert('找不到此編號的詩歌');
        return;
    }
    // Add to queue or replace
    state.queue = [song];
    state.queueIndex = 0;
    updateQueueBar();
    showLyrics(song);
}

// ===== LYRICS =====
function showLyrics(song) {
    const catName = CAT_DISPLAY[state.category];
    document.getElementById('lyrics-category').textContent = catName;
    document.getElementById('lyrics-number').textContent = `${song.id} 首`;
    document.getElementById('lyrics-name').textContent = song.title;
    document.getElementById('lyrics-meta').textContent = formatKey(song.key);
    document.getElementById('lyrics-body').textContent = formatLyrics(song.lyrics);
    showPage('lyrics');
}

function prevSong() {
    navigateSong(-1);
}

function nextSong() {
    navigateSong(1);
}

function navigateSong(direction) {
    if (state.queue.length === 0) return;

    const songs = getSongs(state.category);
    const currentSong = state.queue[state.queueIndex];
    const currentIndex = songs.findIndex(song => song.id === currentSong.id);
    if (currentIndex === -1 || songs.length === 0) return;

    const nextIndex = (currentIndex + direction + songs.length) % songs.length;
    const nextSong = songs[nextIndex];
    state.queue = [nextSong];
    state.queueIndex = 0;
    updateQueueBar();
    showLyrics(nextSong);
}

// ===== CATALOG =====
function renderCatalog(cat, filter = '') {
    const list = document.getElementById('cat-list');
    const songs = getSongs(cat);
    list.innerHTML = '';

    const f = filter.trim().toLowerCase();
    const filtered = songs.filter(s => {
        if (!f) return true;
        return s.id.includes(f) || s.title.toLowerCase().includes(f);
    });

    filtered.forEach(song => {
        const item = document.createElement('div');
        item.className = 'cat-item';
        item.innerHTML = `
            <div class="cat-item-num">${song.id}</div>
            <div class="cat-item-title">${song.title}</div>
            <div class="cat-item-key">${song.key || ''}</div>
        `;
        item.addEventListener('click', () => {
            state.category = cat;
            state.queue = [song];
            state.queueIndex = 0;
            updateQueueBar();
            showLyrics(song);
        });
        list.appendChild(item);
    });
}

function switchCatalogTab(cat) {
    state.category = cat;
    document.querySelectorAll('.cat-tab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.cat === cat);
    });
    const search = document.getElementById('cat-search');
    renderCatalog(cat, search.value);
}

// ===== EVENT LISTENERS =====
document.addEventListener('DOMContentLoaded', () => {
    loadData();

    // Tab switching on dialpad
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.cat));
    });

    // Keypad
    document.querySelectorAll('.key').forEach(btn => {
        btn.addEventListener('click', () => handleKey(btn.dataset.key));
    });

    // Play button
    document.getElementById('btn-play').addEventListener('click', playCurrent);

    // Queue bar -> open catalog
    document.getElementById('queue-bar').addEventListener('click', () => {
        switchCatalogTab(state.category);
        showPage('catalog');
    });

    // Lyrics back
    document.getElementById('btn-back').addEventListener('click', () => {
        state.input = '';
        updatePreview();
        showPage('dialpad');
    });

    // Lyrics controls
    document.getElementById('btn-list').addEventListener('click', () => {
        switchCatalogTab(state.category);
        showPage('catalog');
    });
    document.getElementById('btn-prev').addEventListener('click', prevSong);
    document.getElementById('btn-next').addEventListener('click', nextSong);

    // Catalog back
    document.getElementById('btn-back-cat').addEventListener('click', () => {
        state.input = '';
        updatePreview();
        showPage('dialpad');
    });

    // Catalog tabs
    document.querySelectorAll('.cat-tab').forEach(btn => {
        btn.addEventListener('click', () => switchCatalogTab(btn.dataset.cat));
    });

    // Catalog search
    document.getElementById('cat-search').addEventListener('input', (e) => {
        renderCatalog(state.category, e.target.value);
    });

    // Keyboard support
    document.addEventListener('keydown', (e) => {
        if (document.getElementById('page-dialpad').classList.contains('active')) {
            if (e.key >= '0' && e.key <= '9') handleKey(e.key);
            else if (e.key === 'Backspace') handleKey('del');
            else if (e.key === 'Enter') playCurrent();
        }
    });

    // Swipe gestures on lyrics page
    let touchStartX = 0;
    let touchEndX = 0;
    const lyricsPage = document.getElementById('page-lyrics');
    lyricsPage.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    lyricsPage.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) nextSong(); // swipe left -> next
            else prevSong(); // swipe right -> prev
        }
    }, { passive: true });
});
