# Mandarin Learning Tools

A suite of web applications for learning Chinese characters. The app runs in the browser with Flask serving the frontend. Data persists via localStorage and JSON file exports.

**Quick Start:**
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000/
```

---

## Project Structure

```
├── app.py                      # Flask application with API routes
├── requirements.txt            # Python dependencies
├── serve.py                   # Alternative HTTP server with logging
│
├── templates/                 # HTML pages (served by Flask)
│   ├── index.html            # Main hub and navigation
│   ├── setup.html           # First-time setup wizard
│   ├── mandarin_learner.html # Track known characters, find words
│   ├── can_i_read_this.html  # Analyze text readability
│   ├── study_guide.html      # Generate study materials
│   ├── story_suggester.html  # Find stories at your level
│   ├── story_library.html    # Manage story collection
│   ├── traditional_finder.html # Convert traditional→simplified
│   ├── learning_wizard.html  # Guided 6-step learning workflow
│   ├── pathfinder.html       # Build learning paths (greedy algorithm)
│   └── curriculum_unifier.html # Unified curriculum builder
│
├── static/
│   └── js/
│       └── shared_state.js   # Central state management
│
├── data/
│   ├── dictionary.json        # CC-CEDICT word database
│   ├── stories.json          # Story library
│   ├── stories_data.json     # Story character sets (optimized)
│   ├── hsk_characters.json   # HSK vocabulary lists (1504 chars)
│   ├── trad_simp_map.json    # Traditional→Simplified mapping
│   ├── path_formula_bin.py   # Scoring formula configurations
│   └── path_formula_readme.md # Formula documentation
│
├── source/                     # Content sources (served by Flask API)
│   ├── wiki/
│   │   ├── wiki_data.json   # Wikipedia inverted index
│   │   └── wiki_content/    # Extracted article content
│   └── classics/             # (future: Chinese classics)
│
└── scripts/
    ├── build_wiki_index.py   # Build Wikipedia index from dump
    └── hello_mcp_server.py   # MCP server example (optional)
```

---

## Tools Guide

### index.html - Main Hub
Central navigation page. Links to all tools, data management, workflow recommendations.

### setup.html - First-Time Setup
Initialize required files (shared_state.js, trad_simp_map.json) for new users.

### mandarin_learner.html - Character Tracking
- Add/remove characters manually or extract from text
- Find words you can learn with known characters
- Dictionary lookup (pinyin, definition)
- Export/import character lists

### can_i_read_this.html - Readability Analyzer
- Paste any Chinese text
- Shows % of characters you know (by occurrence and unique)
- Highlights unknown characters
- One-click learn characters
- Convert traditional→simplified
- Save text to story library

### study_guide.html - Study Materials
- Generate flashcards from unknown characters
- Shows pinyin, meaning, compound words, example sentences
- Click characters to mark as known
- Print-friendly output

### story_suggester.html - Story Finder
- Finds stories matched to your level
- Sorts by readability percentage
- Shows learning gap (unknown chars per story)
- Click to view full story

### story_library.html - Story Manager
- CRUD operations on stories
- Import/export story database
- Character extraction
- Accepts incoming stories from "Can I Read This"

### traditional_finder.html - Character Navigator
- Find traditional characters in text
- One-click conversion to simplified
- Add simplified version to known list

### learning_wizard.html - Guided Workflow
Six-step learning experience:
1. **Assessment** - Build known character set
2. **Set Goal** - Define target text
3. **Find Paths** - Build learning path through stories
4. **Curriculum** - Generate study lessons with words and stroke order
5. **Test** - Quiz with paired format (2 targets + 3 distractors)
6. **Complete** - Add passed characters to known set

### pathfinder.html - Path Builder
- Greedy algorithm to find best stories for learning target text
- Real-time progress display
- Export paths as JSON

### curriculum_unifier.html - Unified Builder
- Combines all curriculum building features
- Multiple algorithms (Full/Greedy)
- Multiple modes (Build Path, Generate Pool, Find Clusters)
- API search support (Wikipedia)
- Frequency-based scoring

---

## Data Files

### data/dictionary.json
CC-CEDICT word database (~1.1M entries).
```json
{"word": "学习", "chars": ["学", "习"], "pinyin": "xué2 xí2", "meaning": "to learn; to study"}
```

### data/stories.json
Story library with titles, sources, content, character lists.
```json
{"id": 1, "title": "熊爸爸和怪老", "source": "gushi365", "content": "...", "characters": ["一", "三", "上", ...]}
```

### data/stories_data.json
Optimized version with characters as string.
```json
{"id": 1, "title": "熊爸爸和怪老", "characters": "一三上下不丢两个中为么..."}
```

### data/hsk_characters.json
HSK vocabulary lists for quiz distractors.
```json
{"version": "1.0", "count": 1504, "all": ["爱", "八", "爸", ...]}
```

### data/trad_simp_map.json
Traditional→Simplified character mapping (~2500 pairs).
```json
{"愛": "爱", "學": "学", "國": "国"}
```

---

## Scripts

### scripts/build_wiki_index.py
Builds Wikipedia inverted index from dump files.

```bash
# Download and process Wikipedia dump
python scripts/build_wiki_index.py --download

# Process local file with content extraction
python scripts/build_wiki_index.py --input wiki.xml.bz2 \
  --output source/wiki/wiki_data.json \
  --extract-content \
  --content-dir source/wiki/wiki_content
```

### scripts/hello_mcp_server.py
Optional MCP server example using the `mcp` Python package.

---

## Flask API

### GET /api/sources
List available content sources.

### POST /api/search
Search index for characters.
```json
{"source": "wiki", "chars": ["北", "京"], "limit": 2000}
```

### GET /api/content/<source>/<id>/text
Fetch article content.

---

## State Management

The `MandarinState` class in `shared_state.js` is the central data store. Access via `window.mandarinState`:

```javascript
// Check if character is known
window.mandarinState.has('我'); // boolean

// Add/remove characters
window.mandarinState.addCharacter('我');
window.mandarinState.removeCharacter('我');

// Get all characters as array
window.mandarinState.getCharacters(); // ['我', '你', '好', ...]

// Subscribe to changes
const unsubscribe = window.mandarinState.subscribe((knownChars) => {
    console.log('Characters updated:', knownChars);
});

// File operations
window.mandarinState.exportToFile();
window.mandarinState.importFromFile(file, callback);
window.mandarinState.mergeFromFile(file, callback);
```

---

## Development Patterns

### File Operations
Use Blob API for download, FileReader for upload:

```javascript
// Download
const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url; a.download = 'file.json'; a.click();

// Upload
const reader = new FileReader();
reader.onload = (e) => JSON.parse(e.target.result);
reader.readAsText(file);
```

### Character Extraction
```javascript
const extractChars = (text) => [...new Set(text.match(/[\u4e00-\u9fff]/g))];
```

---

## Future Enhancements

- **Full Wikipedia integration** - Download and index full Chinese Wikipedia
- **Chinese classics** - Process texts like Journey to the West, Dream of Red Chamber
- **Spaced repetition** - Anki-style review scheduling
- **Mobile PWA** - Touch-friendly responsive design
- **Content sources** - News articles, graded readers, user submissions
- **Better dictionary** - Stroke order, audio pronunciation

---

## Troubleshooting

### App won't start
```bash
pip install -r requirements.txt
python app.py
```

### Characters not saving
Check browser localStorage is enabled. Try exporting/importing as JSON backup.

### Quiz has no distractors
Ensure `data/hsk_characters.json` exists and contains characters not in known set.

### Stories not loading
Check `data/stories.json` exists and is valid JSON.

### Wikipedia search not working
Run `python scripts/build_wiki_index.py --download` to build the index.
