#!/usr/bin/env python3
"""
Build word frequency data from stories corpus.
Creates frequency list with occurrence counts for each word.
"""

import json
import pkuseg
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
STORIES_FILE = DATA_DIR / 'stories.json'
OUTPUT_FILE = DATA_DIR / 'word_frequency.json'

def build_word_frequency():
    """Build word frequency from stories corpus."""
    
    print("Loading stories...")
    with open(STORIES_FILE, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    
    print(f"Processing {len(stories)} stories...")
    
    word_counter = Counter()
    
    for i, story in enumerate(stories):
        if i % 500 == 0:
            print(f"Processing story {i+1}/{len(stories)}...")
        
        content = story.get('content', '')
        if content:
            pkuseg_ = pkuseg.pkuseg()
            words = pkuseg_.cut(content)
            for word in words:
                if len(word) >= 2:
                    word_counter[word] += 1
    
    print(f"Found {len(word_counter)} unique words")
    
    frequency_list = []
    for rank, (word, count) in enumerate(word_counter.most_common(), 1):
        frequency_list.append({
            'rank': rank,
            'word': word,
            'count': count
        })
    
    print(f"Writing {len(frequency_list)} words to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(frequency_list, f, ensure_ascii=False, indent=2)
    
    print("Done!")
    print(f"Top 20 most common words:")
    for item in frequency_list[:20]:
        print(f"  {item['rank']:6d} {item['word']:10s} {item['count']:10d}")

if __name__ == '__main__':
    build_word_frequency()