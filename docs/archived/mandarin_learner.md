Last updated: 2026-04-09

# Mandarin Learner - Words by Known Characters

**Source:** `templates/archived/mandarin_learner.html`

## Purpose

Show users words they can learn based on their current known characters. The tool filters the dictionary to find multi-character words where ALL characters are already known, sorted by word length.

Also provides text extraction - paste any Chinese text to extract unique characters for adding to known set.

## Dependencies

- **shared_state.js** - Singleton for known characters
- **data/dictionary.json** - CC-CEDICT word database

## Key Functions

### Learnable Words Filter
```javascript
function updateUI() {
    // Filter learnable words
    let suggestions = dictionary.filter(word => {
        const allCharsKnown = word.chars.every(char => window.mandarinState.has(char));
        const isMultiChar = word.word.length > 1;
        return allCharsKnown && isMultiChar;
    });

    // Sort suggestions by length, then alphabetically
    suggestions.sort((a, b) => {
        if (a.word.length !== b.word.length) return a.word.length - b.word.length;
        return a.localeCompare(b);
    });
}
```

### Character Extraction
```javascript
function extractChineseCharacters(text) {
    const chineseRegex = /[\u4e00-\u9fff]/g;
    const matches = text.match(chineseRegex);
    if (!matches) return new Set();
    return new Set(matches);
}
```

### Merge Extracted with Known
```javascript
function mergeExtractedWithKnown() {
    const newChars = Array.from(lastExtractedChars).filter(ch => !window.mandarinState.has(ch));
    const added = window.mandarinState.addCharacters(newChars);
    // Update UI...
}
```

## Data Flow

1. Page loads → dictionary fetched
2. User adds characters via input OR extracts from text
3. shared_state updates → subscription triggers UI refresh
4. Word list filtered to show only learnable words

## UI Patterns

- **Header**: Gradient purple (#667eea → #764ba2), home button
- **Character tiles**: Pill-shaped badges with remove buttons
- **Word list**: Scrollable list with pinyin and meaning
- **Extract preview**: Shows total/new/already-known counts

## Features

1. **Add single character**: Input field + Add button
2. **Load example**: Pre-populates 37 common characters
3. **Extract from text**: Paste text → extract unique chars → preview → add to known
4. **Save/clear**: Export to file or clear all

## Reuse Ideas

- The "words from known characters" filter is a reusable concept for any vocabulary app
- The extraction preview pattern (show what will be added, with stats) is good UX for bulk operations
- Could power a "recommended next words" feature in other tools
