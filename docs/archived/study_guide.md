# Study Guide Generator

**Source:** `templates/archived/study_guide.html`

## Purpose

Turn unknown characters into a focused study guide with context and compound words. Users load a JSON file of unknown characters (exported from "Can I Read This?") and optionally paste original text to generate printable study cards showing:
- Character
- Pinyin
- English meaning
- Compound words made with known characters
- Example sentences from original text

## Dependencies

- **shared_state.js** - Singleton for known characters
- **data/dictionary.json** - CC-CEDICT word database

## Key Functions

### `getCharInfo(ch)`
```javascript
function getCharInfo(ch) {
    const entry = dictionary.find(e => e.word === ch);
    if (entry) {
        return { pinyin: entry.pinyin, meaning: entry.meaning };
    }
    return { pinyin: "?", meaning: "?" };
}
```

### `findCompoundWords(char)`
Finds 2-character words where one character is the target and the other is already known.
```javascript
function findCompoundWords(char) {
    if (!dictionary) return [];
    const compounds = [];
    for (let word of dictionary) {
        if (word.word.length !== 2) continue;
        const [c1, c2] = word.chars;
        if (c1 === char && window.mandarinState.has(c2)) {
            compounds.push(word);
        } else if (c2 === char && window.mandarinState.has(c1)) {
            compounds.push(word);
        }
    }
    return compounds;
}
```

### `extractSentences(char, text)`
Extracts up to 3 sentences containing the target character from provided text.
```javascript
function extractSentences(char, text) {
    if (!text) return [];
    const sentences = text.split(/[。！？；]/);
    const matches = [];
    for (let sent of sentences) {
        if (sent.includes(char)) {
            let clean = sent.trim();
            if (clean) matches.push(clean + "。");
        }
    }
    return [...new Set(matches)].slice(0, 3);
}
```

### `sortUnknownByCompoundCount(unknownList)`
Sorts unknown characters by number of learnable compound words (descending).
```javascript
function sortUnknownByCompoundCount(unknownList) {
    return unknownList.slice().sort((a, b) => {
        const countA = findCompoundWords(a).length;
        const countB = findCompoundWords(b).length;
        return countB - countA;
    });
}
```

## Data Flow

1. User loads JSON file with unknown characters → `unknownChars` array
2. User optionally pastes original text → `originalText`
3. Generate button triggers:
   - Dictionary loaded via fetch
   - Characters sorted by compound word count
   - For each character: lookup pinyin/meaning, find compounds, extract sentences
   - Render study cards with click-to-learn functionality

## UI Patterns

- **Header**: Gradient purple (#9b59b6), home button
- **Sections**: White cards with shadow, purple borders
- **Buttons**: Primary (purple), secondary (blue), success (green)
- **Study cards**: Print-friendly with page-break-inside: avoid

## Reuse Ideas

- The compound word finder could be extracted as a utility
- Sentence extraction pattern useful for any context-learning feature
- Sorting by "learning readiness" (compound count) could power recommendations
