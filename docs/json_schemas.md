# JSON Schema Reference

This document contains JSON file structure reference for developer context. Load `.sample.json` files instead of full files when only needing structure/context.

## JSON File Inventory

| File | Location | Description |
|------|----------|-------------|
| `dictionary.json` | `data/` | CC-CEDICT word database |
| `stories.json` | `data/` | Story library |
| `stories_data.json` | `data/` | Story character data |
| `trad_simp_map.json` | `data/` | Traditional→simplified character mapping |
| `hsk_characters.json` | `data/` | HSK 2.0 character list |
| `wiki_data.json` | `source/wiki/` | Wikipedia inverted index |

## Sample Files Convention

For each `.json` data file, a matching `<original>.sample.json` exists with the top 2 entries for quick structure reference.

**Purpose**: Developer can load sample files to understand data structure without loading large files.

## Proximal Needed Features

- `source/wiki/wiki_content/*.json` samples - for future article structure reference when working with individual Wikipedia articles

## File Structures

### dictionary.json
```json
{
  "word": "string",
  "chars": ["character array"],
  "pinyin": "string",
  "meaning": "string"
}
```

### stories.json
```json
{
  "id": number,
  "title": "string",
  "source": "string",
  "content": "string",
  "characters": ["character array"]
}
```

### stories_data.json
```json
{
  "id": number,
  "title": "string",
  "source": "string",
  "characters": "string (concatenated chars)"
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

### wiki_data.json
```json
{
  "version": "string",
  "name": "string",
  "description": "string",
  "buildDate": "ISO date string",
  "totalPages": number,
  "pagesWithChars": number,
  "uniqueChars": number,
  "pages": {
    "id": { "title": "string", "chars": ["array"] }
  },
  "index": {
    "char": ["page_id array"]
  }
}
```