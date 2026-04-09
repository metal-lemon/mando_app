Last updated: 2026-04-09

# Documentation Style Guide

When updating documentation, follow these rules to maintain consistency.

## Table of Contents

1. [Last Updated](#1-last-updated--always-update-the-date-at-the-top-when-making-changes)
2. [Headings](#2-headings--use--for-toplevel-sections--for-subsections-never-skip-levels)
3. [Code Blocks](#3-code-blocks--always-specify-language-eg-bash-javascript-json)
4. [File Paths](#4-file-paths--enclose-in-backticks-eg-datahsk_charactersjson)
5. [Lists](#5-lists--use----for-unordered-1-for-ordered-keep-indentation-at-2-spaces)
6. [Tables](#6-tables--use-githubflavoured-markdown-with--and----headers)
7. [Command Examples](#7-command-examples--precede-with--or--to-distinguish-from-output)
8. [API Endpoints](#8-api-endpoints--format-as-get-path-or-post-path-in-bold-or-code)
9. [Preserve All Information](#9-preserve-all-information--when-reorganising-never-delete-facts-only-move-or-consolidate)
10. [Keep TOC Updated](#10-keep-toc-updated--after-any-heading-change-refresh-the-table-of-contents)

---

## 1. Last Updated – Always update the date at the top when making changes

Add or update the date at the very top of the document:

```markdown
Last updated: YYYY-MM-DD

# Document Title
```

---

## 2. Headings – Use `##` for top‑level sections, `###` for subsections. Never skip levels

**Good:**

```markdown
## Overview

### Installation

### Configuration
```

**Bad:**

```markdown
# Overview        (no H1 in docs)

#### Subsection   (skipped H2-H3)
```

---

## 3. Code blocks – Always specify language (e.g., ```bash, ```javascript, ```json)

**Good:**

```bash
pip install -r requirements.txt
python app.py
```

```javascript
const extractChars = (text) => [...new Set(text.match(/[\u4e00-\u9fff]/g))];
```

```json
{"word": "学习", "chars": ["学", "习"], "pinyin": "xué2 xí2"}
```

**Bad:**

```
pip install -r requirements.txt
```

---

## 4. File paths – Enclose in backticks, e.g., `data/hsk_characters.json`

**Good:**

- The file is located in `data/stories.json`
- Edit `templates/index.html`

**Bad:**

- The file is located in data/stories.json
- Edit templates/index.html

---

## 5. Lists – Use `-` for unordered, `1.` for ordered. Keep indentation at 2 spaces

**Good:**

```markdown
- First item
  - Nested item (2 spaces indent)
  - Another nested item
- Second item

1. First ordered item
2. Second ordered item
```

**Bad:**

```markdown
* First item
    - Nested item (wrong indent)
```

---

## 6. Tables – Use GitHub‑flavoured Markdown with `|` and `---` headers

**Good:**

| Column A | Column B |
|---------|---------|
| Value 1 | Value 2 |
| Value 3 | Value 4 |

**Bad:**

```
+-------+-------+
| Col A | Col B |
+=======+=======+
| Val 1 | Val 2 |
+-------+-------+
```

---

## 7. Command examples – Precede with `$` or `>` to distinguish from output

**Good:**

```bash
$ pip install -r requirements.txt
$ python app.py
```

```bash
> python app.py
 * Running on http://localhost:5000/
```

**Bad:**

```
pip install -r requirements.txt
python app.py
```

---

## 8. API endpoints – Format as `GET /path` or `POST /path` in bold or code

**Good:**

- `GET /api/sources` - List available content sources
- `POST /api/search` - Search index for characters
- **Bold** `GET /api/content/<source>/<id>/text`

**Bad:**

- GET api/sources
- POST /api/search
- The /api/search endpoint

---

## 9. Preserve all information – When reorganising, never delete facts; only move or consolidate

- Never delete factual content
- Move information to a more appropriate location if needed
- Merge duplicate sections rather than removing
- Add "(deprecated)" or "(moved to ...)" notes instead of deleting

---

## 10. Keep TOC updated – After any heading change, refresh the Table of Contents

1. Run a "find" for `^##` to list all top-level headings
2. Update the TOC to match
3. Ensure TOC links use the format `[Section Name](#slug)`

**Auto-generating anchor links:** GitHub uses lowercase and dashes for anchor links:

- `## My Section` → `#my-section`
- `## API / Endpoints` → `#api--endpoints`

---

## Quick Reference

| Rule | What to do |
|------|------------|
| 1 | Add at top: `Last updated: YYYY-MM-DD` |
| 2 | Use `##` for main sections, `###` for subsections |
| 3 | Use triple backticks with language: ```bash |
| 4 | Wrap paths in backticks: `data/file.json` |
| 5 | Use `-` or `1.` with 2-space indent for nesting |
| 6 | Use `\|---\|---` for table headers |
| 7 | Prefix commands with `$` |
| 8 | Format as `GET /path` or `POST /path` |
| 9 | Never delete facts; move instead |
| 10 | Update TOC after heading changes |