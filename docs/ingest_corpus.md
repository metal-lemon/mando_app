Last updated: 2026-04-09

# Corpus Intake Tool

Ingests text collections and creates all required companion files for the Flask API.

## Table of Contents

1. [Location](#1-location)
2. [What It Does](#2-what-it-does)
3. [Usage](#3-usage)
4. [Arguments](#4-arguments)
5. [Input Formats](#5-input-formats)
6. [Output Structure](#6-output-structure)
7. [Record Format](#7-record-format)
8. [Example](#8-example)

---

## 1. Location

```
scripts/ingest_corpus.py
```

---

## 2. What It Does

1. **Loads input** from various formats (JSON, JSONL, directory, glob, delimited text)
2. **Extracts Chinese characters** using regex `[\u4e00-\u9fff]`
3. **Deduplicates** records by content
4. **Creates folder structure** automatically in `source/<name>/`
5. **Generates companion files:**

| File | Description |
|------|-------------|
| `<name>.json` | Full content records with `id`, `title`, `source`, `content`, `characters` |
| `<name>_data.json` | Inverted index: `{ "index": { "字": ["1", "2"], ... } }` |
| `<name>_freq.json` | Character frequency: `{ "字": 5, "符": 3, ... }` |
| `<name>_corpus_config.json` | Metadata: `{ "name", "description", "totalRecords", "uniqueChars", "buildDate" }` |
| `<name>.sample.json` | First 50 records with `sample: true` |

---

## 3. Usage

```bash
$ python scripts/ingest_corpus.py -i input.json -n my_corpus -d "My corpus"
```

From directory of text files:

```bash
$ python scripts/ingest_corpus.py -i ./texts/ -n my_corpus
```

From glob pattern:

```bash
$ python scripts/ingest_corpus.py -i "*.txt" -n corpus -o source/
```

From delimited text file:

```bash
$ python scripts/ingest_corpus.py -i long_text.txt -n corpus --delimiter "---"
```

---

## 4. Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `-i`, `--input` | ✓ | - | Input file, directory, or glob pattern |
| `-n`, `--name` | ✓ | - | Source name (used in output filenames) |
| `-o`, `--output` | | `source` | Output directory |
| `-d`, `--description` | | `<name> corpus` | Source description |
| `--delimiter` | | auto | Text delimiter (`---`, `===`, `empty`, `title`) |
| `--sample-size` | | 50 | Number of records in sample file |

---

## 5. Input Formats

| Format | How Delimited |
|--------|--------------|
| JSON array | Each object = one record |
| JSON Lines (.jsonl) | Each line = one JSON object |
| Directory | Each file = one record |
| Glob pattern | Each matched file = one record |
| Plain text | By delimiter (see below) |

### Text Delimiters

- `---` - Horizontal rule
- `===` - Triple equals
- `empty` - Double newline (`\n\n`)
- `title` - First line = title, rest = content

Auto-detected if not specified.

---

## 6. Output Structure

```
source/
└── <name>/
    ├── <name>.json
    ├── <name>_data.json
    ├── <name>_freq.json
    ├── <name>_corpus_config.json
    └── <name>.sample.json
```

---

## 7. Record Format

Input records can have these fields:

```json
{
  "title": "Story Title",
  "content": "Chinese text content...",
  "source": "Author or Source"
}
```

Output records always include:

```json
{
  "id": 1,
  "title": "Story Title",
  "source": "Author or Source",
  "content": "Chinese text content...",
  "characters": ["字", "符", "列", "表"]
}
```

---

## 8. Example

```bash
$ python scripts/ingest_corpus.py -i stories.json -n stories -d "Chinese stories"
```

Output:

```bash
Corpus Intake Tool
========================================
Input:    stories.json
Name:     stories
Output:   ./source/stories/
Description: Chinese stories

Loading records...
  Loaded 100 raw records
Normalizing records...
  98 unique records after deduplication
  Extracting characters...
  Found 523 unique Chinese characters
Building index...
Creating output directory: ./source/stories/
Saving files...
  Saved: ./source/stories/stories.json
  Saved: ./source/stories/stories_data.json
  Saved: ./source/stories/stories_freq.json
  Saved: ./source/stories/stories_corpus_config.json
  Saved: ./source/stories/stories.sample.json

========================================
Complete!
  Total records: 98
  Unique chars: 523
  Output dir: ./source/stories
```