# AGENTS.md - Mandarin Learning Tools

## Project Overview

A suite of client-side web applications for learning Chinese characters. The app runs entirely in the browser with no build step required. Data persists via localStorage and JSON file exports.

## Running the Application

**Note**: The user runs the local server manually. Agents can monitor the application logs while the user runs it.

```bash
# User runs this in their terminal:
python -m http.server 8000

# Or using Node.js if Python not available
npx serve .

# Open in browser
http://localhost:8000/index.html
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
│   ├── stories.json           # Story library
│   ├── trad_simp_map.json     # Traditional→simplified mapping
│   └── stories_data.json      # Story character data
├── source/                     # Content sources (Flask)
│   ├── wiki/
│   │   ├── wiki_data.json     # Inverted index
│   │   └── wiki_content/     # Extracted article content
│   └── classics/
├── docs/
│   ├── json_schemas.md        # JSON file structure reference
│   └── archived/              # Documentation for superseded tools
│       ├── study_guide.md
│       ├── pathfinder.md
│       ├── mandarin_learner.md
│       ├── curriculum_unifier.md
│       └── can_i_read_this.md
├── scripts/
│   └── build_wiki_index.py    # Build Wikipedia index from dump
├── serve.py                   # Optional: HTTP server with log capture
└── AGENTS.md                  # This file
```

## Testing

This is a vanilla HTML/CSS/JS project with no test framework. Manual testing is done by:
1. User runs the local server
2. Open http://localhost:8000 in browser
3. Test features manually in the browser
4. Check browser console (F12) for JavaScript errors

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

### HTML

- Use semantic HTML5 elements (`<header>`, `<section>`, `<main>`)
- Always include `<meta charset="UTF-8">` and `<meta name="viewport">`
- External scripts/styles before closing `</head>`, scripts before `</body>`
- Include `shared_state.js` in all pages that need character data

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <script src="shared_state.js"></script>
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

## Common Tasks

### Add a new page
1. Copy structure from existing page (e.g., `story_library.html`)
2. Include `<script src="shared_state.js"></script>`
3. Add link in `index.html` toolbox modal
4. Add route in `app.py` if needed

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
Update all `fetch()` calls and file download paths. Default is `data/` for dictionary and stories.

### File Location Conventions
- **Canonical location for stories**: `data/stories.json`
- **Canonical location for dictionary**: `data/dictionary.json`
- **Canonical location for character data**: `data/trad_simp_map.json`
- When exporting, use timestamped backup filenames (e.g., `stories_backup_2026-03-28.json`)
- All pages should read from `data/stories.json` - do not use root-level `stories.json`
