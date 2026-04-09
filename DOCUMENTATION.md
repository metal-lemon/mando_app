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
│   ├── index.html            # Main hub (3 stacked boxes + toolbox modal)
│   ├── setup.html           # First-time setup wizard
│   ├── learning_wizard.html  # Guided 6-step learning workflow
│   ├── traditional_finder.html # Convert traditional→simplified (toolbox)
│   ├── story_suggester.html  # Find stories at your level (toolbox)
│   └── story_library.html    # Manage story collection (toolbox)
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
Simplified page with 3 stacked horizontal boxes:
1. **Setup** (thin box) - First-time setup
2. **Learning Wizard** (tall box) - Featured, 6-step guided workflow
3. **Toolbox** (thin box) - Opens modal with additional tools

### setup.html - First-Time Setup
Initialize required files (shared_state.js, trad_simp_map.json) for new users.

### learning_wizard.html - Guided Workflow (Featured)
Six-step learning experience:
1. **Assessment** - Build known character set
2. **Set Goal** - Define target text
3. **Find Paths** - Build learning path through stories
4. **Curriculum** - Generate study lessons with words and stroke order
5. **Test** - Quiz with paired format (2 targets + 3 HSK distractors)
6. **Complete** - Add passed characters to known set

### Toolbox Modal Tools (accessed from index.html)

#### traditional_finder.html - Character Navigator
- Find traditional characters in text
- One-click conversion to simplified
- Add simplified version to known list

#### story_suggester.html - Story Finder
- Finds stories matched to your level
- Sorts by readability percentage
- Shows learning gap (unknown chars per story)
- Click to view full story

#### story_library.html - Story Manager
- CRUD operations on stories
- Import/export story database
- Character extraction
- Accepts incoming stories

### Archived Tools Documentation

Documentation for superseded tools is preserved in `docs/archived/`:

| Tool | Docs Location | Description |
|------|---------------|-------------|
| `mandarin_learner` | `docs/archived/mandarin_learner.md` | Words by known characters |
| `can_i_read_this` | `docs/archived/can_i_read_this.md` | Text readability analyzer |
| `study_guide` | `docs/archived/study_guide.md` | Generate study materials |
| `pathfinder` | `docs/archived/pathfinder.md` | Learning path builder |
| `curriculum_unifier` | `docs/archived/curriculum_unifier.md` | Multi-source curriculum builder |

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
HSK vocabulary lists for quiz distractors. Contains HSK 2.0 (2001 standard) all 6 levels combined.
```json
{"version": "1.0", "source": "HSK 2.0 (2001 standard)", "description": "All 6 HSK levels combined into single set", "count": 2663, "all": ["爱", "八", ...]}
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

## Planned: Simplify Index Page and Archive Redundant Pages

### Goal
Simplify the main index page to show only 3 items, and move redundant tools to an archive folder.

### New Index Page Layout
```
┌─────────────────────────────────────────────┐
│           Mandarin Learning Tools              │
├─────────────────────────────────────────────┤
│                   Setup                      │
├─────────────────────────────────────────────┤
│                                             │
│              Learning Wizard                  │
│           (taller, featured)                │
│                                             │
├─────────────────────────────────────────────┤
│                  Toolbox                      │
└─────────────────────────────────────────────┘
```

### Toolbox Modal Contents
- Traditional Finder
- Story Suggester
- Story Library

### Files to Archive (documentation moved to `docs/archived/`)
| Tool | Description |
|------|-------------|
| `mandarin_learner` | Words by known characters |
| `can_i_read_this` | Text readability analyzer |
| `study_guide` | Generate study materials |
| `pathfinder` | Learning path builder |
| `curriculum_unifier` | Multi-source curriculum builder |

### Files to Keep (Active)
- `index.html` - Simplified main page (3 stacked boxes)
- `learning_wizard.html` - Full guided workflow (featured)
- `setup.html` - First-time setup
- `traditional_finder.html` - In toolbox modal
- `story_suggester.html` - In toolbox modal
- `story_library.html` - In toolbox modal

### Implementation Steps (Completed)
1. ✅ Fix git merge conflict in index.html (lines 394-407)
2. ✅ Create documentation in `docs/archived/`:
   - mandarin_learner.md
   - can_i_read_this.md
   - study_guide.md
   - pathfinder.md
   - curriculum_unifier.md
3. ✅ Delete original HTML files from `templates/archived/`
4. ✅ Delete empty `templates/archived/` folder
5. ✅ Rewrite `index.html` with 3 stacked horizontal boxes
6. ✅ Add Toolbox modal with links to: Traditional Finder, Story Suggester, Story Library
7. ✅ Update app.py routes (remove broken wiki_curriculum_builder route, update archive path)
8. ✅ Update this DOCUMENTATION.md to reflect new structure

### Current Project Structure
```
├── templates/
│   ├── index.html            # Simplified (3 boxes + toolbox modal)
│   ├── setup.html           # First-time setup
│   ├── learning_wizard.html  # Featured (6-step guided workflow)
│   ├── traditional_finder.html # Toolbox
│   ├── story_suggester.html  # Toolbox
│   └── story_library.html   # Toolbox
│
├── docs/
│   └── archived/            # Documentation for superseded tools
│       ├── mandarin_learner.md
│       ├── can_i_read_this.md
│       ├── study_guide.md
│       ├── pathfinder.md
│       └── curriculum_unifier.md
```

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

---

## Planned Updates

### HSK Characters JSON Update
**Status**: Not yet implemented

1. **Update `data/hsk_characters.json`**:
   - Correct `count` from 1504 → 2663 (actual unique character count)
   - Add `source` detail: "HSK 2.0 (2001 standard), all 6 levels combined"
   - Optionally add `description` field for clarity

2. **Update `DOCUMENTATION.md`**:
   - Fix example count from 1504 to 2663
   - Add note about HSK version 2.0 and all 6 levels in one set

---

## Hypothetical Future Features

### Separate HSK Level Arrays
The current `hsk_characters.json` contains all 6 HSK levels combined into a single `all` array. A future enhancement could structure the data by level:

```json
{
  "version": "1.0",
  "source": "HSK 2.0 (2001 standard)",
  "description": "All 6 levels combined",
  "count": 2663,
  "all": ["爱", "八", ...],
  "levels": {
    "1": ["爱", "八", "爸", ...],
    "2": [...],
    "3": [...],
    "4": [...],
    "5": [...],
    "6": [...]
  }
}
```

This would allow:
- Targeting quizzes at specific HSK levels
- Progress tracking by level
- Filtering story difficulty by HSK level
