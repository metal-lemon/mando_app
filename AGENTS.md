# AGENTS.md - Mandarin Learning Tools

## Project Overview

A suite of web applications for learning Chinese characters. The app runs in the browser with Flask serving the frontend. Data persists via localStorage and JSON file exports.

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py

# Open in browser
http://localhost:5000/
```

## File Structure

```
├── app.py                      # Flask application with API routes
├── requirements.txt            # Python dependencies
├── templates/                  # HTML pages (served by Flask)
│   ├── index.html             # Main hub (3 stacked boxes + toolbox)
│   ├── setup.html             # First-time setup wizard
│   ├── learning_wizard.html    # Guided 6-step learning workflow
│   ├── traditional_finder.html # Convert trad→simp (toolbox)
│   ├── story_suggester.html   # Find stories by level (toolbox)
│   └── story_library.html     # Manage stories (toolbox)
├── static/
│   └── js/
│       └── shared_state.js     # Central state management
├── data/
│   ├── dictionary.json         # CC-CEDICT word database
│   ├── trad_simp_map.json     # Traditional→simplified mapping
│   └── hsk_characters.json   # HSK vocabulary for quizzes
├── source/                     # Content sources (Flask API)
│   ├── stories/               # Stories corpus
│   │   ├── stories.json       # Full content
│   │   ├── stories_data.json  # Inverted index
│   │   ├── stories_freq.json  # Character frequency
│   │   ├── stories_corpus_config.json  # Metadata
│   │   └── stories.sample.json # Sample for testing
│   ├── wiki/                  # Wikipedia corpus
│   │   ├── wiki.json          # Full content
│   │   ├── wiki_data.json     # Inverted index
│   │   ├── wiki_freq.json     # Character frequency
│   │   ├── wiki_corpus_config.json  # Metadata
│   │   └── wiki.sample.json   # Sample for testing
│   └── <future>/              # New sources follow same pattern
├── scripts/
│   ├── build_wiki_index.py    # Build Wikipedia index from dump
│   ├── ingest_corpus.py      # Corpus intake tool (hidden)
│   └── hello_mcp_server.py    # MCP server (optional)
├── docs/
│   ├── style_guide.md       # Documentation style guide
│   ├── ingest_corpus.md     # Corpus intake tool
│   ├── json_schemas.md      # JSON file structure reference
│   ├── path_formula_readme.md # Path formula documentation
│   └── archived/           # Documentation for superseded tools
└── AGENTS.md                  # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/sources` | GET | List available content sources (auto-discovered from source/) |
| `/api/search` | POST | Search index for characters (specify source in body) |
| `/api/content/<source>/<id>` | GET | Fetch full content record |
| `/api/content/<source>/<id>/text` | GET | Fetch plain text content |
| `/api/batch_content` | POST | Fetch multiple records |
| `/api/segment` | POST | Segment Chinese text using pkuseg |
| `/api/words-by-frequency` | POST | Get words sorted by frequency (rarest first) |

### Source Discovery

The Flask API auto-discovers sources from the `source/` directory. Each source must have:
- `<source>_corpus_config.json` (preferred) or `<source>_data.json` (legacy)
- `<source>.json` (content file, optional but needed for full functionality)

Response from `/api/sources` includes:
```json
{
  "id": "stories",
  "name": "Stories",
  "description": "Chinese stories corpus",
  "totalRecords": 2679,
  "uniqueChars": 4652,
  "hasContent": true,
  "hasIndex": true,
  "hasFreq": true
}
```

### Source Companion Files

Every content source in `source/<name>/` follows the same companion file pattern:

| File | Description | Required |
|------|-------------|----------|
| `<name>.json` | Full content records (array of objects with id, title, source, content, characters) | Yes |
| `<name>_data.json` | Inverted index: mapping from character to list of record IDs | Yes |
| `<name>_freq.json` | Character frequency: how many records contain each character | Yes |
| `<name>_corpus_config.json` | Metadata: name, description, totalRecords, uniqueChars, buildDate | Yes |
| `<name>.sample.json` | Small subset for testing (same format as main file with sample: true) | Yes |
| `<name>_inverted_index.bin` | Binary optimized index (optional, for large corpora) | No |

### Adding a New Source

**Option 1: Use ingest_corpus.py (recommended)**
The corpus intake tool automatically creates all required files from text input:
```bash
# From JSON array
python scripts/ingest_corpus.py -i input.json -n my_corpus -d "My corpus"

# From directory of text files
python scripts/ingest_corpus.py -i ./texts/ -n my_corpus

# From glob pattern
python scripts/ingest_corpus.py -i "*.txt" -n corpus -o source/

# From delimited text file
python scripts/ingest_corpus.py -i long_text.txt -n corpus --delimiter "---"
```

**Option 2: Manual process**
1. Create `source/<name>/` directory
2. Generate `<name>.json` with content records
3. Generate `<name>_data.json` with inverted index (script required)
4. Generate `<name>_freq.json` with character frequency
5. Generate `<name>_corpus_config.json` with metadata
6. Generate `<name>.sample.json` with small subset
7. Source auto-discovered by Flask API - no code changes needed

### Search Request Example
```json
POST /api/search
{
    "source": "wiki",
    "chars": ["北", "京", "中"],
    "limit": 2000
}
```

### Search Response Example
```json
{
    "source": "wiki",
    "query_chars": ["北", "京", "中"],
    "total_candidates": 150,
    "candidates": [
        {"id": "12345", "title": "北京", "coverage": 3, "matched_chars": ["北", "京", "中"]},
        ...
    ]
}
```

## Documentation Style Guide

All documentation follows the rules in `docs/style_guide.md`. When updating docs, apply these 10 rules:

| # | Rule | Apply As |
|---|------|----------|
| 1 | Last updated | Add `Last updated: YYYY-MM-DD` at top |
| 2 | Headings | Use `##` top-level, `###` subsections |
| 3 | Code blocks | All code in ```bash/```json/```javascript fences |
| 4 | File paths | Enclose in backticks: `data/stories.json` |
| 5 | Lists | `-` unordered, `1.` ordered, 2-space indent |
| 6 | Tables | GitHub-flavored: `\|---\|---\|` |
| 7 | Commands | Prefix with `$` or `>` |
| 8 | API endpoints | `GET /path` or `POST /path` in bold |
| 9 | Preserve info | Never delete facts; move/consolidate only |
| 10 | Keep TOC | Refresh after heading changes |

### Documentation Files

| File | Description |
|------|-------------|
| `DOCUMENTATION.md` | Main project documentation |
| `docs/style_guide.md` | Style guide reference |
| `docs/ingest_corpus.md` | Corpus intake tool docs |
| `docs/json_schemas.md` | JSON file structure reference |
| `docs/path_formula_readme.md` | Path formula documentation |
| `docs/archived/*.md` | Documentation for superseded tools |

### Adding New Documentation

1. Create new `.md` file in appropriate location
2. Add `Last updated: YYYY-MM-DD` at top
3. Include Table of Contents
4. Follow all 10 style rules
5. Update `AGENTS.md` if adding new workflow docs

## Testing

1. Start Flask server: `python app.py`
2. Open http://localhost:5000/ in browser
3. Test features manually in the browser
4. Check browser console (F12) for JavaScript errors
5. Check Flask terminal for API request logs

## Code Style Guidelines

### JavaScript

- **Naming**: camelCase for variables and functions, PascalCase for classes
- **Constants**: UPPER_SNAKE_CASE for true constants (e.g., `STATE_VERSION`)
- **Quotes**: Single quotes for strings, template literals for interpolation
- **Semicolons**: Always use semicolons
- **Braces**: K&R style (opening brace on same line)
- **Indentation**: 4 spaces

```javascript
// Good
const STATE_VERSION = "1.0";
const STORAGE_KEYS = {
    KNOWN_CHARS: "mandarin_known_chars",
    LAST_UPDATED: "mandarin_last_updated"
};

class MandarinState {
    constructor() {
        this.listeners = new Set();
        this.knownChars = new Set();
        this.load();
    }
}

// Bad
const stateVersion = "1.0"; // should be UPPER_SNAKE_CASE
const storageKeys = { ... }; // should be UPPER_SNAKE_CASE
```

## Naming Conventions Glossary

This glossary defines all naming conventions used throughout the codebase.

| Type | Convention | Example |
|------|------------|---------|
| Module constants | UPPER_SNAKE_CASE | STATE_VERSION, STORAGE_KEYS |
| Local variables | UPPER_SNAKE_CASE | const DATA, const READER |
| Functions/methods | camelCase | getCharacters(), extractChars() |
| Classes | PascalCase | MandarinState, FileReader |
| CSS classes | kebab-case | .button-group, .file-status |

### References
- Module constants defined in `static/js/shared_state.js`
- See Section: Code Style Guidelines above

### HTML

- Use semantic HTML5 elements (`<header>`, `<section>`, `<main>`)
- Always include `<meta charset="UTF-8">` and `<meta name="viewport">`
- External scripts/styles before closing `</head>`, scripts before `</body>`
- Include shared_state.js from static path: `<script src="/static/js/shared_state.js"></script>`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <script src="/static/js/shared_state.js"></script>
</head>
<body>
    <!-- content -->
    <script>
        // page-specific JS
    </script>
</body>
</html>
```

### CSS

- **Naming**: kebab-case for class names (e.g., `.button-group`, `.file-status`)
- **Organization**: Group related styles; use flexbox/grid for layout
- **Responsive**: Include `@media` queries for mobile (breakpoint at 600px or 768px)
- **Colors**: Use named colors or hex; consistent gradient headers across pages

```css
/* Good */
.button-group {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 15px 0;
}

.file-status.success {
    background-color: #e8f5e9;
    border-left-color: #4CAF50;
}

/* Bad */
.btnGroup { } /* should be kebab-case */
```

## Core Patterns

### Global State (Singleton)

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
```

### Character Extraction

Use the Chinese character regex pattern `[\u4e00-\u9fff]` to find Chinese characters:

```javascript
function extractCharacters(text) {
    const chineseRegex = /[\u4e00-\u9fff]/g;
    const matches = text.match(chineseRegex);
    if (!matches) return [];
    return [...new Set(matches)];
}
```

### File Export Pattern

Use Blob API for downloading JSON files:

```javascript
function exportToFile(data, filename) {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}
```

### File Import Pattern

Use FileReader API for loading JSON files:

```javascript
function loadFromFile(file, callback) {
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const data = JSON.parse(e.target.result);
            callback(null, data);
        } catch (err) {
            callback(err);
        }
    };
    reader.onerror = () => callback(new Error("File read error"));
    reader.readAsText(file, 'UTF-8');
}
```

### Flask API Pattern

For Flask-powered pages, use fetch() to call API endpoints:

```javascript
// List available sources
const res = await fetch('/api/sources');
const data = await res.json();
console.log(data.sources);

// Search for characters
const res = await fetch('/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        source: 'wiki',
        chars: ['北', '京'],
        limit: 2000
    })
});
const data = await res.json();
console.log(data.candidates);

// Fetch article content
const res = await fetch('/api/content/wiki/12345/text');
const article = await res.json();
console.log(article.title, article.text);
```

## JSON Data Formats

### Character List
```json
{
    "version": "1.0",
    "date": "2024-01-01T00:00:00.000Z",
    "characters": ["我", "你", "好"],
    "count": 3
}
```

### Story Database Entry
```json
{
    "id": 1,
    "title": "Story Title",
    "source": "Source or Author",
    "content": "Chinese text content...",
    "characters": ["字", "符", "列", "表"]
}
```

### Source Index Format
```json
{
    "version": "1.0",
    "name": "Wikipedia",
    "description": "Chinese Wikipedia articles",
    "buildDate": "2026-04-02T00:00:00.000Z",
    "totalPages": 1400000,
    "pagesWithChars": 500000,
    "uniqueChars": 12000,
    "pages": {
        "12345": { "title": "北京", "chars": ["北", "京"] }
    },
    "index": {
        "北": ["12345", "67890"],
        "京": ["12345", "11111"]
    }
}
```

### Article Content Format
```json
{
    "id": "12345",
    "title": "北京",
    "text": "北京是中国的首都...",
    "chars": ["北", "京", "是", "中", "国", "的", "首", "都"]
}
```

## Error Handling

- Wrap file operations in try/catch blocks
- Log errors to console with `console.error()`
- Show user-friendly messages via alerts or status divs
- Always validate JSON structure before processing

```javascript
try {
    const data = JSON.parse(jsonString);
    if (!data.characters || !Array.isArray(data.characters)) {
        throw new Error("Invalid format");
    }
    // process data
} catch (e) {
    console.error("Failed to process:", e);
    alert("Error: " + e.message);
}
```

## Accessibility

- Use semantic HTML elements
- Include descriptive button text (not just icons)
- Ensure color contrast meets WCAG guidelines
- Support keyboard navigation for forms

## Performance Tips

- Cache DOM queries (e.g., `document.getElementById()` results)
- Use event delegation where multiple similar elements exist
- Debounce input handlers for search/filter operations
- Use `analysisCache` Map to avoid re-analyzing unchanged data
- For large data, use Flask API endpoints instead of loading entire files

## Common Tasks

### Add a new page
1. Copy structure from existing page (e.g., `story_library.html`)
2. Place in `templates/` directory
3. Include `<script src="/static/js/shared_state.js"></script>`
4. Add link in `templates/index.html` toolbox modal
5. Add route in `app.py` if custom handling needed

### Add a new content source
1. Process source data with `scripts/ingest_corpus.py` (recommended) or `scripts/build_wiki_index.py` (for Wikipedia)
2. Output goes to `source/<name>/` with all companion files
3. Source will auto-appear in wiki_curriculum_builder dropdown

### Add a new button style
Add to existing button styles in the page's `<style>` block:
```css
button.secondary {
    background-color: #48bb78;
}
button.secondary:hover {
    background-color: #38a169;
}
```

### Modify data folder location
Update Flask route in `app.py` and all `fetch()` calls.

### File Location Conventions
- **Canonical location for stories**: `data/stories.json`
- **Canonical location for dictionary**: `data/dictionary.json`
- **Canonical location for character data**: `data/trad_simp_map.json`
- **Source data**: `source/<name>/<name>_data.json`
- **Source content**: `source/<name>/<name>_content/`
- When exporting, use timestamped backup filenames (e.g., `stories_backup_2026-03-28.json`)
- All pages should read from `data/stories.json` - do not use root-level `stories.json`

## Wiki Curriculum Builder

The Wiki Curriculum Builder uses content sources as libraries to find reading material for learning specific characters.

### Setup Process

1. **Download Wikipedia dump**: Download from one of these sources:
   - **XML bz2** (recommended): Download from Wikimedia dumps
     ```bash
     python scripts/build_wiki_index.py --download
     ```
   - **ZIM file**: Download from Kiwix (e.g., `wikipedia_zh_all_maxi.zim`)

2. **Build the index**: The script parses Wikipedia pages, extracts Chinese characters, and builds an inverted index:
   ```bash
   # For XML bz2
   python scripts/build_wiki_index.py --input zhwiki-latest-pages-articles.xml.bz2

   # For ZIM file (requires zim-tools or libzim)
   python scripts/build_wiki_index.py --input wikipedia_zh_all_maxi.zim
   ```

3. **Build with content extraction** (for Flask app):
   ```bash
   python scripts/build_wiki_index.py --input dump.xml.bz2 \
     --output source/wiki/wiki_data.json \
     --extract-content \
     --content-dir source/wiki/wiki_content
   ```

4. **Start Flask and access**: Run `python app.py` and open http://localhost:5000/wiki_curriculum_builder

#### ZIM Support Requirements

For processing ZIM files, install one of:
- **libzim Python bindings**: `pip install libzim` (may require compilation tools)
- **zim-tools** (includes `zimdump` CLI):
  - Ubuntu/Debian: `sudo apt install zim-tools`
  - macOS: `brew install zim-tools`
  - Windows: Download from https://github.com/kiwix/kiwix-tools/releases

### Browser Tool Workflow

1. Start Flask server: `python app.py`
2. Open http://localhost:5000/wiki_curriculum_builder
3. Select content source from dropdown (e.g., Wikipedia)
4. Enter target text (what you want to learn to read)
5. System identifies unknown characters (target - known from shared_state)
6. Flask API searches inverted index for pages containing unknown chars
7. Count coverage: how many unknown chars each page contains
8. Sort by coverage, return top 2000 candidates
9. Click "Read" to fetch specific article content
10. Export candidate pool as JSON or CSV

### Future Enhancements

- **Stage 2**: Jaccard clustering of candidates by character overlap
- **Stage 3**: Path optimization to minimize jumpsize
- **Stage 4**: Wikipedia article preview within the tool

## Future Development Ideas

### Corpus Ingestion Enhancements

- **Improved text file parsing**: Auto-detect story boundaries with smarter heuristics (title patterns, numbered sections, paragraph density analysis)
- **Format auto-detection**: Automatically detect input format without requiring CLI flags
- **Incremental updates**: Support adding new records to existing corpus without full rebuild
- **Batch processing**: Process multiple input files into separate sources in one run
- **Validation mode**: Check existing corpus files for required fields and data integrity
