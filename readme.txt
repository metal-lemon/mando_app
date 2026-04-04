================================================================================
MANDARIN LEARNING TOOLS v2.02 - USER GUIDE
================================================================================

A comprehensive suite of web-based tools for learning Chinese characters, with
Flask serving the frontend and local data persistence.

================================================================================
TABLE OF CONTENTS
================================================================================

1. Quick Start
2. File Structure
3. Tool Descriptions
4. API Endpoints
5. Workflow Guide
6. ZIM Indexer (Wikipedia)
7. File Formats
8. Troubleshooting
9. Version History

================================================================================
1. QUICK START
================================================================================

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py

# Open in browser
http://localhost:5000/

================================================================================
2. FILE STRUCTURE
================================================================================

v2.02/
├── app.py                      # Flask application with API routes
├── requirements.txt            # Python dependencies
├── templates/                  # HTML pages (served by Flask)
│   ├── index.html              # Home page with tool links
│   ├── setup.html              # One-click setup tool
│   ├── mandarin_learner.html   # Track known characters & vocabulary
│   ├── can_i_read_this.html    # Text readability analyzer
│   ├── study_guide.html        # Study guide generator
│   ├── story_suggester.html    # Story recommendation tool
│   ├── story_library.html      # Story management (add/edit/delete/export)
│   ├── traditional_finder.html # Traditional→simplified converter
│   ├── curriculum_builder.html # Build reading curriculum from texts
│   ├── lite_builder.html       # Lightweight curriculum builder
│   ├── wiki_curriculum_builder.html  # Wikipedia-based curriculum
│   └── curriculum_unifier.html # Merge multiple curricula
├── static/
│   └── js/
│       └── shared_state.js     # Central state management
├── data/
│   ├── dictionary.json         # CC-CEDICT word database (~20MB)
│   ├── stories.json            # Story library (~15MB)
│   ├── stories_data.json      # Story character data
│   └── trad_simp_map.json     # Traditional→simplified mapping
├── source/                     # Large content sources (Flask)
│   ├── wiki/
│   │   ├── wiki_data.json     # Inverted index (optional)
│   │   └── wiki_content/     # Extracted article content (optional)
│   └── classics/
│       ├── classics_data.json
│       └── classics_content/
├── scripts/
│   ├── build_wiki_index.py    # Build Wikipedia index from XML/ZIM
│   └── hello_mcp_server.py    # MCP server (optional)
└── serve.py                   # Optional: HTTP server with log capture

================================================================================
3. TOOL DESCRIPTIONS
================================================================================

CORE LEARNING TOOLS
-------------------

1. MANDARIN LEARNER (mandarin_learner.html)
   - Track known characters
   - Auto-saves to localStorage
   - Shows words you can learn based on known characters
   - Export/import character lists
   - Displays pinyin and English definitions

2. CAN I READ THIS? (can_i_read_this.html)
   - Paste any Chinese text
   - Shows two percentages:
     * Occurrence % – based on total character occurrences
     * Unique % – based on distinct characters
   - Click unknown characters to add them
   - Color-coded readability advice

3. STUDY GUIDE GENERATOR (study_guide.html)
   - Load unknown characters from text analysis
   - Shows pinyin and meaning for each character
   - Finds compound words using known characters
   - Extracts example sentences from text
   - Click to mark characters as known

4. STORY SUGGESTER (story_suggester.html)
   - Stories ranked by difficulty (occurrence % or unique %)
   - Toggle sorting between metrics
   - Split long stories into 300-character chunks
   - Click to read full story with analysis

5. STORY LIBRARY (story_library.html)
   - View all stories with ID, title, source, length
   - Add new stories with auto-character extraction
   - Edit or delete stories
   - Export database as JSON

6. TRADITIONAL FINDER (traditional_finder.html)
   - Load traditional→simplified mapping
   - Paste text to highlight traditional characters
   - Convert text to simplified with one click
   - Click characters to add simplified versions

CURRICULUM BUILDERS
-------------------

7. CURRICULUM BUILDER (curriculum_builder.html)
   - Build reading curriculum from any text
   - Extracts characters and finds matching stories
   - Creates ordered learning path

8. LITE BUILDER (lite_builder.html)
   - Lightweight version of curriculum builder
   - Streamlined interface for quick curriculum creation

9. WIKI CURRICULUM BUILDER (wiki_curriculum_builder.html)
   - Use Wikipedia articles as reading material
   - Search for articles containing target characters
   - Select articles to build curriculum
   - Requires wiki_data.json index file

10. CURRICULUM UNIFIER (curriculum_unifier.html)
    - Merge multiple curricula
    - Combine character coverage from different sources

SETUP
-----
11. SETUP (setup.html)
    - One-click setup for initial configuration
    - Creates shared_state.js if missing

================================================================================
4. API ENDPOINTS
================================================================================

The Flask app provides these API endpoints:

GET  /api/sources                    List available content sources
POST /api/search                     Search index for characters
GET  /api/content/<source>/<id>/text  Fetch article content

Search Request Example:
----------------------
POST /api/search
{
    "source": "wiki",
    "chars": ["北", "京", "中"],
    "limit": 2000
}

Search Response Example:
----------------------
{
    "source": "wiki",
    "query_chars": ["北", "京", "中"],
    "total_candidates": 150,
    "candidates": [
        {"id": "12345", "title": "北京", "coverage": 3, "matched_chars": ["北", "京", "中"]}
    ]
}

================================================================================
5. WORKFLOW GUIDE
================================================================================

COMPLETE LEARNING LOOP
----------------------

1. BUILD YOUR BASE
   → Mandarin Learner: Add characters you already know
   → Export your character list (optional, for backup)

2. ANALYZE A TEXT YOU WANT TO READ
   → Can I Read This?: Paste the text
   → See occurrence % and unique %
   → Click unknown characters you actually know

3. CREATE STUDY MATERIALS
   → Study Guide Generator: Load unknown characters
   → Paste original text for context
   → Generate guide with pinyin, meanings, examples
   → Click characters you learn during study

4. UPDATE YOUR KNOWLEDGE
   → Export updated character list from Study Guide
   → Import into Mandarin Learner (or it auto-syncs)

5. BUILD YOUR STORY LIBRARY
   → Story Library: Load or create stories.json
   → Add stories you want to read

6. FIND YOUR NEXT TEXT
   → Story Suggester: Stories ranked automatically
   → Sort by occurrence % or unique %
   → Read and enjoy!

WIKIPEDIA-BASED LEARNING
------------------------

1. Build the Wikipedia index (see Section 6)
2. Start Flask server
3. Open wiki_curriculum_builder.html
4. Enter text you want to learn to read
5. System finds Wikipedia articles containing target characters
6. Click "Read" to view article
7. Export candidates as JSON for curriculum builder

================================================================================
6. ZIM INDEXER (WIKIPEDIA)
================================================================================

The ZIM indexer builds a character-to-article mapping from a Wikipedia ZIM file.

ZIM FILE LOCATION:
-----------------
C:\Users\Lapushka\Documents\MandarinCorpus\Wikipedia\
├── wikipedia_zh_all_maxi_2025-09.zim   (25GB input)
├── scripts/
│   └── build_index_from_zim.py          (indexer script)
└── data/
    └── wiki_zh_char_index.db            (SQLite output)

USAGE:
------
# Test mode (first 1000 articles)
python scripts\build_index_from_zim.py --test

# With custom limit
python scripts\build_index_from_zim.py --limit 50000

# Full build (~12-24 hours for 2.8M articles)
python scripts\build_index_from_zim.py

REQUIRES:
---------
libzim Python bindings: pip install libzim

SQLITE SCHEMA:
--------------
CREATE TABLE pages (page_id INTEGER PRIMARY KEY, title TEXT, url TEXT);
CREATE TABLE char_page (char TEXT, page_id INTEGER);
CREATE INDEX idx_char ON char_page (char);

================================================================================
7. FILE FORMATS
================================================================================

CHARACTER LIST FORMAT
--------------------
Simple array: ["我","学","习","中","文"]

Object format:
{
  "version": "1.0",
  "date": "2024-01-01T00:00:00.000Z",
  "characters": ["我","学","习","中","文"],
  "count": 5
}

STORY DATABASE FORMAT (data/stories.json)
-----------------------------------------
[
  {
    "id": 1,
    "title": "Story Title",
    "source": "Source or Author",
    "content": "Story content in Chinese...",
    "characters": ["字","符","列","表"]
  }
]

SOURCE INDEX FORMAT (source/<name>/<name>_data.json)
----------------------------------------------------
{
  "version": "1.0",
  "name": "Wikipedia",
  "description": "Chinese Wikipedia articles",
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

================================================================================
8. TROUBLESHOOTING
================================================================================

PROBLEM: "Error loading dictionary"
SOLUTION:
- Ensure Flask server is running
- Verify data/dictionary.json exists
- Check Flask terminal for errors

PROBLEM: Shared state not syncing
SOLUTION:
- Run setup.html to recreate missing files
- Clear browser cache and refresh
- Verify shared_state.js is loading (check browser console)

PROBLEM: Stories not loading after adding
SOLUTION:
- After adding a story, you MUST reload the file
- Click "Load Story Database" again and select the downloaded file

PROBLEM: Wiki Curriculum Builder shows "No sources available"
SOLUTION:
- Build the Wikipedia index using build_index_from_zim.py
- Ensure wiki_data.json is in source/wiki/
- Restart Flask server

PROBLEM: Wikipedia index search is slow
SOLUTION:
- The index is loaded into memory on startup
- For large indexes, consider using SQLite version (wiki_zh_char_index.db)
- The Flask app currently uses JSON index only

================================================================================
9. VERSION HISTORY
================================================================================

Version 2.02 (April 2026)
- Migrated to Flask-based architecture
- Added curriculum_unifier.html for merging curricula
- Updated wiki_curriculum_builder.html
- Consolidated file structure (templates/, data/, scripts/, source/)
- Added SQLite ZIM indexer option

Version 2.01 (March 2026)
- Added curriculum_builder.html and lite_builder.html
- Enhanced wiki_curriculum_builder.html
- Added jump_formula.py for path optimization

Version 2.0 (March 2025)
- Complete rewrite with Flask
- Added Story Library and Story Suggester
- Added shared state for automatic sync across tools
- Added setup.html for one-click installation

Version 1.0 (Initial Release)
- Mandarin Learner tool
- Can I Read This? analyzer
- Study Guide Generator
- Traditional Character Finder
- Basic export/import functionality

================================================================================
SUPPORT & RESOURCES
================================================================================

- CC-CEDICT Dictionary: https://www.mdbg.net/chinese/dictionary
- Wikipedia ZIM Downloads: https://download.kiwix.org/zim/wikipedia/
- Python Download: https://www.python.org/downloads/
- libzim: pip install libzim

================================================================================
