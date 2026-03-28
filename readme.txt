================================================================================
MANDARIN LEARNING TOOLS - COMPLETE USER GUIDE
================================================================================

A comprehensive suite of web-based tools to help you learn Chinese characters,
improve reading comprehension, and manage a personal story library.

================================================================================
TABLE OF CONTENTS
================================================================================

1. Overview
2. File Structure
3. Quick Start Guide
4. Tool Descriptions
5. Complete Workflow Tutorial
6. Setup Instructions
7. Story Library – Detailed Guide
8. File Formats
9. Troubleshooting
10. Customization
11. Version History

================================================================================
1. OVERVIEW
================================================================================

This suite includes six interconnected tools that work together to create a
complete Chinese learning environment:

1. Mandarin Learner – Track known characters and discover new vocabulary
2. Can I Read This? – Analyze texts to see what you can read (dual percentage)
3. Study Guide Generator – Create focused study materials
4. Story Suggester – Find stories ranked by difficulty (occurrence / unique %)
5. Story Library – Manage your personal story database (add, edit, delete, export)
6. Traditional Finder – Identify traditional Chinese characters and convert to simplified

All tools automatically share your character data and work offline in your
browser. Your data is stored locally and can be exported for backup.

================================================================================
2. FILE STRUCTURE
================================================================================

Place all files in the same folder:

mandarin_app/
├── index.html                  (Home page with tool links)
├── setup.html                  (One-click setup tool)
├── mandarin_learner.html       (Track characters & vocabulary)
├── can_i_read_this.html        (Text readability analyzer – occurrence & unique %)
├── study_guide.html            (Study guide generator)
├── story_suggester.html        (Story recommendation tool – dual percentages, sortable)
├── story_library.html          (Story management – add, edit, delete, export)
├── traditional_finder.html     (Traditional character detector & converter)
├── shared_state.js             (Shared data management – auto-created)
├── stories.json                (Story database – auto-created or user-supplied)
├── traditional_chars.json      (Traditional character list – auto-created)
├── trad-simp.txt               (Optional: full traditional‑simplified mapping)
├── dictionary.json             (CC-CEDICT dictionary – must be created)
└── README.txt                  (This file)

================================================================================
3. QUICK START GUIDE
================================================================================

STEP 1: Run Setup (First Time Only)
------------------------------------
1. Start the local web server (see Setup Instructions below)
2. Open http://localhost:8000/index.html
3. Click "Run Setup" on the orange banner
4. The setup tool will create all required files automatically
5. Click "Go to Home Page" when complete

STEP 2: Load Dictionary
------------------------------------
1. Open Mandarin Learner
2. If dictionary.json is missing, follow instructions in Section 6
3. Once loaded, you'll see words available to learn

STEP 3: Start Building Your Character List
------------------------------------
1. In Mandarin Learner, type a Chinese character (e.g., 我)
2. Click "Add" or press Enter
3. The app will suggest words you can learn
4. Continue adding characters you know

STEP 4: Analyze Your First Text
------------------------------------
1. Open Can I Read This?
2. Load your character list (auto-loaded from shared state)
3. Paste Chinese text you want to read
4. Click "Analyze Text" to see:
   - Occurrence percentage (based on total characters)
   - Unique percentage (based on distinct characters)
5. Click on unknown characters to add them to your list

STEP 5: Generate a Study Guide
------------------------------------
1. Open Study Guide Generator
2. Load unknown characters from Can I Read This? (or use exported file)
3. Paste the original text for context
4. Click "Generate Study Guide"
5. Click on characters you know to mark them learned
6. Export updated list when done

STEP 6: Build Your Story Library
------------------------------------
1. Open Story Library
2. Click "Load Story Database" and select stories.json (or create new by adding)
3. Add stories using "Add New Story" – characters are auto‑extracted
4. Edit or delete stories as needed
5. Use "Export Database" to save your library

STEP 7: Find Stories to Read
------------------------------------
1. Open Story Suggester
2. If stories.json is in the folder, it loads automatically
3. View stories ranked by difficulty (default: occurrence %)
4. Toggle sorting between occurrence % and unique % using the buttons
5. Enable "Chunk Mode" for long stories
6. Click "Read Story" to view with full analysis

================================================================================
4. TOOL DESCRIPTIONS
================================================================================

TOOL 1: MANDARIN LEARNER (mandarin_learner.html)
------------------------------------------------
Purpose: Track known characters and discover new vocabulary

Features:
- Add/remove individual characters
- Auto-saves to localStorage (shared across all tools)
- Shows words you can learn based on known characters
- Export/import character lists
- Extract characters from any text and add them
- Displays pinyin and English definitions

Use when: Building your character knowledge base

TOOL 2: CAN I READ THIS? (can_i_read_this.html)
------------------------------------------------
Purpose: Analyze texts to determine reading readiness

Features:
- Paste any Chinese text
- Shows two percentages:
  * Occurrence percentage – based on total character occurrences
  * Unique percentage – based on distinct characters
- Lists unknown characters
- Click on unknown characters to add them
- Color-coded readability advice (98%+, 95%+, 90%+, <90% occurrence)
- Export unknown characters or updated known list

Use when: Testing if you can read a specific text

TOOL 3: STUDY GUIDE GENERATOR (study_guide.html)
------------------------------------------------
Purpose: Create personalized study materials

Features:
- Load unknown characters from text analysis
- Shows pinyin and meaning for each character
- Finds compound words using your known characters
- Extracts example sentences from your text
- Sort characters by number of compound words
- Click to mark characters as known
- Export updated known list

Use when: Preparing to study unknown characters

TOOL 4: STORY SUGGESTER (story_suggester.html)
------------------------------------------------
Purpose: Find appropriate reading materials

Features:
- Stories ranked by difficulty (occurrence % or unique %)
- Toggle sorting between the two metrics
- Split long stories into 300-character chunks
- Shows both percentages on each story card
- Click to read full story with detailed analysis
- Auto-loads stories.json from folder

Use when: Looking for your next book or article to read

TOOL 5: STORY LIBRARY (story_library.html)
------------------------------------------------
Purpose: Manage your story database

Features:
- View all stories with ID, title, source, length, character count
- Add new stories with auto-character extraction
- Edit existing stories
- Delete stories with confirmation
- Export the entire database as JSON
- Load a custom stories.json file

Use when: Building and maintaining your collection of reading materials

TOOL 6: TRADITIONAL FINDER (traditional_finder.html)
------------------------------------------------
Purpose: Identify and convert traditional Chinese characters

Features:
- Load a traditional‑simplified mapping (from trad-simp.txt or JSON)
- Paste any text to highlight traditional characters
- Convert the text to simplified with one click
- Click on characters to add simplified versions to your known list
- Export found traditional characters

Use when: Working with traditional Chinese texts

================================================================================
5. COMPLETE WORKFLOW TUTORIAL
================================================================================

Complete Learning Loop:

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
   → Generate guide with pinyin, meanings, and examples
   → Click characters you learn during study

4. UPDATE YOUR KNOWLEDGE
   → Export updated character list from Study Guide
   → Import into Mandarin Learner (or it auto-syncs)
   → Your knowledge base grows

5. BUILD YOUR STORY LIBRARY
   → Story Library: Load or create stories.json
   → Add stories you want to read
   → Edit or delete as needed

6. FIND YOUR NEXT TEXT
   → Story Suggester: Stories are ranked automatically
   → Sort by occurrence % (ease of reading) or unique % (vocabulary breadth)
   → Pick one with high percentage
   → Read and enjoy!
   → Repeat the cycle!

================================================================================
6. SETUP INSTRUCTIONS
================================================================================

RUNNING THE LOCAL WEB SERVER (REQUIRED)
----------------------------------------
IMPORTANT: You MUST run through a web server, not by double-clicking files.

Option A: Using Python (Recommended)
1. Install Python from python.org
2. Open Command Prompt/Terminal
3. Navigate to your app folder:
   cd C:\Users\YourName\Desktop\mandarin_app
4. Start the server:
   python -m http.server
5. Open browser to: http://localhost:8000/index.html
6. Press Ctrl+C to stop the server

Option B: Using VS Code Live Server
1. Install "Live Server" extension
2. Right-click index.html and select "Open with Live Server"

GENERATING DICTIONARY.JSON
---------------------------
The dictionary is required for word suggestions and compound word lookup.

1. Download CC-CEDICT from https://www.mdbg.net/chinese/dictionary
2. Open mandarin_learner.html via the web server
3. Open browser console (F12) and paste the conversion script (see Appendix)
4. Select your cedict.txt file when prompted
5. Download the generated dictionary.json to your app folder

Note: The script is available in the console or can be provided separately.

================================================================================
7. STORY LIBRARY – DETAILED GUIDE
================================================================================

HOW TO ADD A NEW STORY (STEP BY STEP)
---------------------------------------
1. Open Story Library
2. Click "Load Story Database" and select your stories.json file
   (If you don't have one yet, you can add a story anyway – it will create one)

3. Click "Add New Story" button
4. Fill in the form:
   - Title: Give your story a name
   - Source: Where it's from (optional)
   - Content: Paste the Chinese text

5. Watch the character preview appear automatically
   - Shows all unique Chinese characters found in your text

6. Click "Save Story"
   - The tool automatically finds the next available ID number
   - Your browser downloads an updated stories.json file

7. IMPORTANT: Click "Load Story Database" again and select the newly downloaded file
   - This reloads the database with your new story

8. Your story now appears in the library.

HOW TO EDIT OR DELETE STORIES
-------------------------------
1. In Story Library, find the story you want to edit or delete
2. Use the buttons:
   - 👁️ View – See the full story content
   - ✏️ Edit – Modify title, source, or content
   - 🗑️ Delete – Remove the story (with confirmation)

3. After editing or deleting, a new file downloads automatically
4. Reload the file to see your changes

================================================================================
8. FILE FORMATS
================================================================================

CHARACTER LIST FORMAT (JSON)
----------------------------
All tools accept these formats:

Simple array:
["我","学","习","中","文"]

Object format:
{
  "version": "1.0",
  "date": "2024-01-01T00:00:00.000Z",
  "characters": ["我","学","习","中","文"],
  "count": 5
}

STORY DATABASE FORMAT (stories.json)
------------------------------------
[
  {
    "id": 1,
    "title": "Story Title",
    "source": "Source or Author",
    "content": "Story content in Chinese...",
    "characters": ["字","符","列","表"]
  }
]

TRADITIONAL MAP FORMAT (trad-simp.txt or JSON)
----------------------------------------------
Text file format (trad-simp.txt):
傳統  简化
體    体

JSON format (trad_simp_map.json):
{
  "體": "体",
  "國": "国"
}

================================================================================
9. TROUBLESHOOTING
================================================================================

PROBLEM: "Error loading dictionary"
SOLUTION:
- Ensure you're using the web server (http://localhost:8000)
- Verify dictionary.json is in the same folder
- Check that dictionary.json is valid JSON

PROBLEM: Shared state not syncing
SOLUTION:
- Verify shared_state.js is in the folder
- Run setup.html to recreate missing files
- Clear browser cache and refresh

PROBLEM: Stories not loading after adding
SOLUTION:
- After adding a story, you MUST reload the file
- Click "Load Story Database" again and select the downloaded file
- This is a browser security feature – files must be explicitly loaded

PROBLEM: Only one percentage appears in Story Suggester
SOLUTION:
- Make sure you have loaded stories.json
- The story suggester shows both percentages on each card
- If the sorting toggle doesn't appear, ensure the script loaded correctly

PROBLEM: Traditional Finder doesn't detect characters
SOLUTION:
- Load a mapping file (trad-simp.txt or JSON) using the buttons
- The tool will try to auto‑load trad-simp.txt if present
- If using the built‑in list, ensure it's loaded (click "Use Built‑in Map")

================================================================================
10. CUSTOMIZATION
================================================================================

ADDING YOUR OWN STORIES (CORRECT WORKFLOW)
-------------------------------------------
1. Open Story Library
2. Load your existing stories.json (or start fresh)
3. Click "Add New Story"
4. Enter title, source (optional), and content
5. Characters are auto-extracted and previewed
6. Click "Save Story" – file downloads automatically
7. IMPORTANT: Reload the downloaded file using "Load Story Database"
8. Your story appears in the library and will be available in Story Suggester

MODIFYING THE TRADITIONAL MAPPING
-----------------------------------------
1. Obtain a file with traditional‑simplified pairs (e.g., trad-simp.txt)
2. Place it in your app folder
3. Open Traditional Finder; it will auto‑load the file
4. Alternatively, load a JSON map using "Load Custom Map"

CHANGING CHUNK SIZE
-------------------
In story_suggester.html, modify this line:
const chunks = splitIntoChunks(story.content, 300); // Change 300 to desired size

ADDING HSK LEVELS TO DICTIONARY
-------------------------------
You can extend dictionary.json with an "hsk" field:
{ "word": "学习", "chars": ["学","习"], "pinyin": "xue2 xi2", "meaning": "to study", "hsk": 1 }

================================================================================
11. VERSION HISTORY
================================================================================

Version 2.1 (March 2025)
- Added Story Library as a separate tool for managing story database
- Enhanced Can I Read This? with dual percentages (occurrence & unique)
- Enhanced Story Suggester with dual percentages and sortable metrics
- Improved Traditional Finder with direct trad-simp.txt loading and conversion
- Refined UI and consolidated navigation

Version 2.0 (March 2025)
- Added Story Suggester with library management
- Added shared state for automatic sync across tools
- Added setup.html for one-click installation
- Added edit/delete capabilities for stories

Version 1.0 (Initial Release)
- Mandarin Learner tool
- Can I Read This? analyzer
- Study Guide Generator
- Traditional Character Finder
- Basic export/import functionality

================================================================================
APPENDIX: DICTIONARY CONVERSION SCRIPT
================================================================================

Copy and paste this into browser console (F12) to generate dictionary.json:

const input = document.createElement('input');
input.type = 'file';
input.accept = '.txt';
input.onchange = e => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const lines = content.split('\n');
        const dictMap = new Map();
        for (let line of lines) {
            if (line.length === 0 || line.startsWith('#')) continue;
            const firstSpace = line.indexOf(' ');
            const simplified = line.substring(0, firstSpace);
            const afterSimplified = line.substring(firstSpace + 1);
            const secondSpace = afterSimplified.indexOf(' ');
            const rest = afterSimplified.substring(secondSpace + 1);
            const pinyinMatch = rest.match(/\[(.*?)\]/);
            const pinyin = pinyinMatch ? pinyinMatch[1] : '';
            const meaningMatch = rest.match(/\/(.*?)\//);
            const meaning = meaningMatch ? meaningMatch[1] : '';
            const chars = Array.from(simplified);
            if (chars.length === 0) continue;
            if (!dictMap.has(simplified)) {
                dictMap.set(simplified, {
                    word: simplified,
                    chars: chars,
                    pinyin: pinyin,
                    meaning: meaning
                });
            }
        }
        const dictionary = Array.from(dictMap.values());
        const json = JSON.stringify(dictionary, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'dictionary.json';
        a.click();
        URL.revokeObjectURL(url);
        console.log(`Converted ${dictionary.length} unique words.`);
    };
    reader.readAsText(file, 'UTF-8');
};
input.click();

================================================================================
SUPPORT & RESOURCES
================================================================================

- CC-CEDICT: https://www.mdbg.net/chinese/dictionary
- Unicode Chinese Character Range: \u4e00-\u9fff
- Python Download: https://www.python.org/downloads/

================================================================================