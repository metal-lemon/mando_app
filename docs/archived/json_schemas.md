Last updated: 2026-04-09

> **DEPRECATED**: This file is archived as of 2026-04-11. The information has been superseded by AGENTS.md. File locations are now defined in AGENTS.md under "File Location Conventions".

# JSON Schema Reference

This document contains JSON file structure reference for developer context. Load `.sample.json` files instead of full files when only needing structure/context.

## Table of Contents

1. [JSON File Inventory](#1-json-file-inventory)
2. [Source Companion Files](#2-source-companion-files)
3. [Sample Files Convention](#3-sample-files-convention)
4. [File Structures](#4-file-structures)

---

## 1. JSON File Inventory

| File | Location | Description |
|------|----------|-------------|
| `dictionary.json` | `data/` | CC-CEDICT word database |
| `stories.json` | `source/stories/` | Story library (moved from data/) |
| `stories_data.json` | `source/stories/` | Story character data (inverted index) |
| `stories_freq.json` | `source/stories/` | Character frequency |
| `stories_corpus_config.json` | `source/stories/` | Corpus metadata |
| `stories.sample.json` | `source/stories/` | Sample for testing |
| `trad_simp_map.json` | `data/` | Traditional→simplified character mapping |
| `hsk_characters.json` | `data/` | HSK 2.0 character list |
| `wiki.json` | `source/wiki/` | Wikipedia articles |
| `wiki_data.json` | `source/wiki/` | Wikipedia inverted index |
| `wiki_freq.json` | `source/wiki/` | Character frequency |
| `wiki_corpus_config.json` | `source/wiki/` | Corpus metadata |
| `wiki.sample.json` | `source/wiki/` | Sample for testing |

---

## 2. Source Companion Files

Every content source in `source/<name>/` follows the same companion file pattern:

| File | Description | Required |
|------|-------------|----------|
| `<name>.json` | Full content records | Yes |
| `<name>_data.json` | Inverted index | Yes |
| `<name>_freq.json` | Character frequency | Yes |
| `<name>_corpus_config.json` | Metadata | Yes |
| `<name>.sample.json` | Sample for testing | Yes |
| `<name>_inverted_index.bin` | Binary index (optional) | No |

---

## 3. Sample Files Convention

For each `.json` data file, a matching `<original>.sample.json` exists with a small subset for quick structure reference.

---

## 4. File Structures

### Content File (<name>.json)

```json
[
  {
    "id": "string or number",
    "title": "string",
    "source": "string",
    "content": "string",
    "characters": ["character array"]
  }
]
```

### Inverted Index (<name>_data.json)

```json
{
  "version": "string",
  "name": "string",
  "description": "string",
  "totalRecords": number,
  "uniqueChars": number,
  "buildDate": "ISO date string",
  "index": {
    "character": ["id array"]
  }
}
```

### Character Frequency (<name>_freq.json)

```json
{
  "version": "string",
  "name": "string",
  "description": "string",
  "totalCharacters": number,
  "frequency": {
    "character": number
  }
}
```

### Corpus Config (<name>_corpus_config.json)

```json
{
  "version": "string",
  "name": "string",
  "description": "string",
  "source": "string",
  "totalRecords": number,
  "totalUniqueCharacters": number,
  "averageCharactersPerRecord": number,
  "buildDate": "ISO date string",
  "fileFormats": ["json", "json_gz"],
  "companionFiles": ["file list"]
}
```

### Sample File (<name>.sample.json)

```json
{
  "version": "string",
  "name": "string",
  "description": "string",
  "totalRecords": number,
  "sample": true,
  "records": [...]
}
```

### dictionary.json

```json
{
  "word": "string",
  "chars": ["character array"],
  "pinyin": "string",
  "meaning": "string"
}
```

### trad_simp_map.json

```json
{
  "traditional_char": "simplified_char"
}
```

### hsk_characters.json

```json
{
  "version": "string",
  "source": "string",
  "count": number,
  "all": ["character array"]
}
```