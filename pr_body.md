## Summary

Converts the Mandarin Learning Tools app to a Flask application with server-side APIs for handling large data sources.

### Changes

- **Flask app structure** - `app.py` with REST API endpoints, `requirements.txt` for dependencies
- **Template directory** - All HTML pages moved to `templates/` for Flask rendering
- **Static files** - JS served from `static/js/`
- **API endpoints**:
  - `GET /api/sources` - List available content sources
  - `POST /api/search` - Server-side search using inverted index
  - `GET /api/content/<source>/<id>/text` - Fetch article content on demand
- **Build script updates** - `build_wiki_index.py` now supports `--extract-content` for creating article content files
- **Source directory** - `source/` structure for multiple content types (wiki, classics, news, etc.)

### Why

The original browser-only app couldn't handle multi-GB Wikipedia dumps. This conversion allows:
- Server-side search returns only top 2000 candidates (~2MB)
- Article content fetched on-demand only when user requests it
- Support for multiple large content sources without browser memory limits

### Testing

```
pip install -r requirements.txt
python app.py
# Open http://localhost:5000/
```

### Future Work

- Add more content sources (classics, news, etc.)
- Process actual Wikipedia dump for real data
