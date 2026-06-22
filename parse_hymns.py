#!/usr/bin/env python3
"""
Parse hymn text files extracted from PDFs into structured JSON.
Usage: python3 parse_hymns.py
Output: data/hymns.json
"""
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_DIR = os.path.join(BASE_DIR, "..", "tmp_pdf_txt")
OUT_DIR = os.path.join(BASE_DIR, "data")

def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def is_chord_line(text):
    """Heuristic: if line is mostly ascii letters/symbols and has no Chinese, it's likely chords."""
    if not text:
        return False
    # If it contains Chinese, it's not a pure chord line
    if has_chinese(text):
        return False
    # If it's just letters, numbers, and common chord symbols
    clean = text.replace(' ', '').replace('\t', '')
    if len(clean) < 3:
        return True
    # Check if mostly ascii
    ascii_count = sum(1 for c in clean if ord(c) < 128)
    if ascii_count / len(clean) > 0.9:
        return True
    return False

def clean_lyrics_line(text):
    """Remove chord symbols and keep mainly Chinese text."""
    # Remove common chord patterns like xgtyluxa, a;’styluxa, etc.
    # Strategy: extract Chinese characters and some punctuation
    result = []
    i = 0
    while i < len(text):
        c = text[i]
        # Keep Chinese chars
        if '\u4e00' <= c <= '\u9fff':
            result.append(c)
        # Keep common punctuation
        elif c in '，。、；：？！「」『』（）…—～‧':
            result.append(c)
        # Keep digits for verse markers like 一) 二)
        elif c.isdigit():
            result.append(c)
        # Keep ) for verse markers
        elif c == ')':
            result.append(c)
        # Keep 副 for chorus marker
        elif c == '副':
            result.append(c)
        # Keep spaces (will trim later)
        elif c == ' ':
            result.append(' ')
        i += 1
    cleaned = ''.join(result).strip()
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def parse_大本詩歌(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    songs = []
    current = None
    in_toc = True

    for i, line in enumerate(lines):
        raw = line.rstrip('\n')
        stripped = raw.strip()

        # Detect end of TOC by finding first actual song with key signature
        if in_toc and re.match(r'^[A-G][b#]?\s+\d/\d$', stripped):
            in_toc = False
            # The song title should be 1-3 lines above
            # But we already passed it; backtrack
            for back in range(1, 5):
                if i - back >= 0:
                    prev = lines[i - back].strip()
                    m = re.match(r'^(\d{3})\s+(.+)$', prev)
                    if m and '....' not in prev and len(prev) < 60:
                        current = {
                            'id': m.group(1),
                            'title': m.group(2).strip(),
                            'key': stripped,
                            'lyrics': []
                        }
                        break
            continue

        if in_toc:
            continue

        # Detect new song start
        m = re.match(r'^(\d{3})\s+(.+)$', stripped)
        if m and '....' not in stripped and len(stripped) < 60:
            if current and current['lyrics']:
                songs.append(current)
            current = {
                'id': m.group(1),
                'title': m.group(2).strip(),
                'key': '',
                'lyrics': []
            }
            continue

        if not current:
            continue

        # Detect key signature
        if re.match(r'^[A-G][b#]?\s+\d/\d$', stripped):
            current['key'] = stripped
            continue

        # Skip chord-only lines
        if is_chord_line(stripped):
            continue

        # Clean lyrics
        cleaned = clean_lyrics_line(stripped)
        if cleaned and len(cleaned) > 3:
            current['lyrics'].append(cleaned)

    if current and current['lyrics']:
        songs.append(current)

    return songs

def parse_新歌頌詠(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    songs = []
    current = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect: 新歌頌詠.docx 001
        m = re.match(r'^新歌頌詠\.docx\s+(\d+)$', stripped)
        if m:
            if current and current['lyrics']:
                songs.append(current)
            current = {
                'id': m.group(1).zfill(3),
                'title': '',
                'key': '',
                'lyrics': []
            }
            continue

        if not current:
            continue

        # First non-empty after marker is title
        if not current['title'] and stripped and not stripped.startswith('---'):
            current['title'] = stripped
            continue

        # Detect key signature
        key_match = re.match(r'^([A-G][b#]?\s+\d/\d)(.*)$', stripped)
        if key_match and not current['key']:
            current['key'] = key_match.group(1).strip()
            # If there's remaining text after the key, treat it as lyrics
            remainder = key_match.group(2).strip()
            if remainder and has_chinese(remainder):
                cleaned = clean_lyrics_line(remainder)
                if cleaned and len(cleaned) > 3:
                    current['lyrics'].append(cleaned)
            continue

        # Skip chord-only lines
        if is_chord_line(stripped):
            continue

        # Clean lyrics
        cleaned = clean_lyrics_line(stripped)
        if cleaned and len(cleaned) > 3:
            current['lyrics'].append(cleaned)

    if current and current['lyrics']:
        songs.append(current)

    return songs

def parse_新詩(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    songs = []
    current = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect: 新詩.docx 001  or  010 乘上聖靈的浪潮
        m1 = re.match(r'^新詩\.docx\s+(\d+)$', stripped)
        m2 = re.match(r'^(\d{3})\s+(.+)$', stripped)

        if m1:
            if current and current['lyrics']:
                songs.append(current)
            current = {
                'id': m1.group(1).zfill(3),
                'title': '',
                'key': '',
                'lyrics': []
            }
            continue
        elif m2 and not stripped.startswith('---') and len(stripped) < 60 and has_chinese(stripped):
            # This might be a song start without docx marker
            if current and not current['title']:
                current['title'] = m2.group(2).strip()
                continue
            elif current and current['lyrics']:
                songs.append(current)
                current = {
                    'id': m2.group(1),
                    'title': m2.group(2).strip(),
                    'key': '',
                    'lyrics': []
                }
                continue

        if not current:
            continue

        # First non-empty after marker (if no title yet)
        if not current['title'] and stripped and not stripped.startswith('---') and has_chinese(stripped):
            current['title'] = stripped
            continue

        # Detect key signature
        key_match = re.match(r'^([A-G][b#]?\s+\d/\d)(.*)$', stripped)
        if key_match:
            current['key'] = key_match.group(1).strip()
            remainder = key_match.group(2).strip()
            if remainder and has_chinese(remainder):
                cleaned = clean_lyrics_line(remainder)
                if cleaned and len(cleaned) > 3:
                    current['lyrics'].append(cleaned)
            continue

        # Skip chord-only lines
        if is_chord_line(stripped):
            continue

        # Clean lyrics
        cleaned = clean_lyrics_line(stripped)
        if cleaned and len(cleaned) > 3:
            current['lyrics'].append(cleaned)

    if current and current['lyrics']:
        songs.append(current)

    return songs

def parse_補充本(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    songs = []
    current = None
    in_toc = True

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect end of TOC
        if in_toc and re.match(r'^\d{4}\s+', stripped):
            # Check if next line is a key signature
            if i + 1 < len(lines):
                next_l = lines[i + 1].strip()
                if re.match(r'^[A-G][b#]?\s+\d/\d$', next_l):
                    in_toc = False
                    m = re.match(r'^(\d{4})\s+(.+)$', stripped)
                    if m:
                        current = {
                            'id': m.group(1),
                            'title': m.group(2).strip(),
                            'key': next_l,
                            'lyrics': []
                        }
                    continue

        if in_toc:
            continue

        # Detect new song
        m = re.match(r'^(\d{4})\s+(.+)$', stripped)
        if m and len(stripped) < 60:
            if current and current['lyrics']:
                songs.append(current)
            # Check if next line is key
            key = ''
            if i + 1 < len(lines):
                next_l = lines[i + 1].strip()
                if re.match(r'^[A-G][b#]?\s+\d/\d$', next_l):
                    key = next_l
            current = {
                'id': m.group(1),
                'title': m.group(2).strip(),
                'key': key,
                'lyrics': []
            }
            continue

        if not current:
            continue

        # Detect key signature
        key_match = re.match(r'^([A-G][b#]?\s+\d/\d)(.*)$', stripped)
        if key_match and not current['key']:
            current['key'] = key_match.group(1).strip()
            remainder = key_match.group(2).strip()
            if remainder and has_chinese(remainder):
                cleaned = clean_lyrics_line(remainder)
                if cleaned and len(cleaned) > 3:
                    current['lyrics'].append(cleaned)
            continue

        # Skip chord-only lines
        if is_chord_line(stripped):
            continue

        # Clean lyrics
        cleaned = clean_lyrics_line(stripped)
        if cleaned and len(cleaned) > 3:
            current['lyrics'].append(cleaned)

    if current and current['lyrics']:
        songs.append(current)

    return songs


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    data = {
        '大本詩歌': parse_大本詩歌(os.path.join(TXT_DIR, '大本詩歌.txt')),
        '新歌頌詠': parse_新歌頌詠(os.path.join(TXT_DIR, '新歌頌詠.txt')),
        '新詩': parse_新詩(os.path.join(TXT_DIR, '新詩.txt')),
        '補充本': parse_補充本(os.path.join(TXT_DIR, '補充本詩歌_2012版.txt')),
    }

    # Validation & stats
    for category, songs in data.items():
        print(f"{category}: {len(songs)} songs parsed")
        if songs:
            print(f"  Example: #{songs[0]['id']} {songs[0]['title']} (key: {songs[0]['key']}, lyrics: {len(songs[0]['lyrics'])} lines)")

    # Save
    out_path = os.path.join(OUT_DIR, 'hymns.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {out_path}")

if __name__ == '__main__':
    main()
