#!/usr/bin/env python3
"""
Mandarin Learning Tools - Flask Application

A Flask web app for learning Chinese characters with support for multiple
large content sources (Wikipedia, Classics, News, etc.) via server-side APIs.

Usage:
    python app.py

Then open http://localhost:5000 in your browser.
"""

import json
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, Response

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR / 'source'
DATA_DIR = BASE_DIR / 'data'


def discover_sources():
    """Auto-discover available sources from the source/ directory structure."""
    sources = []
    
    if not SOURCE_DIR.exists():
        return sources
    
    for source_path in SOURCE_DIR.iterdir():
        if not source_path.is_dir():
            continue
        
        data_file = source_path / f'{source_path.name}_data.json'
        
        if data_file.exists():
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                sources.append({
                    'id': source_path.name,
                    'name': metadata.get('name', source_path.name.title()),
                    'description': metadata.get('description', ''),
                    'totalPages': metadata.get('totalPages', 0),
                    'pagesWithChars': metadata.get('pagesWithChars', 0),
                    'uniqueChars': metadata.get('uniqueChars', 0),
                    'buildDate': metadata.get('buildDate', ''),
                })
            except (json.JSONDecodeError, IOError):
                sources.append({
                    'id': source_path.name,
                    'name': source_path.name.title(),
                    'description': '',
                    'totalPages': 0,
                    'pagesWithChars': 0,
                    'uniqueChars': 0,
                    'buildDate': '',
                })
        else:
            sources.append({
                'id': source_path.name,
                'name': source_path.name.title(),
                'description': 'No index file found',
                'totalPages': 0,
                'pagesWithChars': 0,
                'uniqueChars': 0,
                'buildDate': '',
            })
    
    return sources


def load_source_index(source_id):
    """Load the inverted index for a source."""
    source_path = SOURCE_DIR / source_id
    data_file = source_path / f'{source_id}_data.json'
    
    if not data_file.exists():
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/<page_name>')
def serve_page(page_name):
    """Serve HTML pages from templates directory."""
    template_path = Path(__file__).parent / 'templates' / f'{page_name}.html'
    
    if template_path.exists():
        return render_template(f'{page_name}.html')
    
    archived_path = Path(__file__).parent / 'templates' / 'archived' / f'{page_name}.html'
    if archived_path.exists():
        return render_template(f'archived/{page_name}.html')
    
    return f"Page not found: {page_name}", 404


@app.route('/api/sources')
def api_sources():
    """Get list of available content sources."""
    sources = discover_sources()
    return jsonify({
        'sources': sources,
        'count': len(sources)
    })


@app.route('/api/search', methods=['POST'])
def api_search():
    """
    Search for content matching given characters.
    
    Request body (JSON):
        source: str - Source ID (e.g., 'wiki', 'classics')
        chars: list - List of characters to match
        limit: int - Maximum results to return (default 2000)
    
    Returns:
        JSON with ranked list of candidate pages
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    source_id = data.get('source')
    chars = data.get('chars', [])
    limit = min(int(data.get('limit', 2000)), 5000)
    
    if not source_id:
        return jsonify({'error': 'Source is required'}), 400
    
    if not chars:
        return jsonify({'error': 'Characters list is required'}), 400
    
    index_data = load_source_index(source_id)
    
    if not index_data:
        return jsonify({'error': f'Source not found: {source_id}'}), 404
    
    index = index_data.get('index', {})
    pages = index_data.get('pages', {})
    
    page_coverage = {}
    
    for char in chars:
        posting_list = index.get(char, [])
        
        for page_id in posting_list:
            if page_id not in page_coverage:
                page_coverage[page_id] = set()
            page_coverage[page_id].add(char)
    
    candidates = []
    for page_id, matched_chars in page_coverage.items():
        page_data = pages.get(page_id)
        if page_data:
            candidates.append({
                'id': page_id,
                'title': page_data.get('title', ''),
                'chars': page_data.get('chars', []),
                'matched_chars': list(matched_chars),
                'coverage': len(matched_chars)
            })
    
    candidates.sort(key=lambda x: x['coverage'], reverse=True)
    candidates = candidates[:limit]
    
    return jsonify({
        'source': source_id,
        'query_chars': chars,
        'total_candidates': len(candidates),
        'candidates': candidates
    })


@app.route('/api/content/<source_id>/<page_id>')
def api_content(source_id, page_id):
    """
    Fetch content for a specific page.
    
    Returns the extracted article content as JSON.
    """
    content_dir = SOURCE_DIR / source_id / f'{source_id}_content'
    
    if not content_dir.exists():
        return jsonify({'error': 'Content directory not found'}), 404
    
    content_file = content_dir / f'{page_id}.json'
    
    if not content_file.exists():
        return jsonify({'error': f'Content not found: {page_id}'}), 404
    
    return send_from_directory(content_dir, f'{page_id}.json', mimetype='application/json')


@app.route('/api/content/<source_id>/<page_id>/text')
def api_content_text(source_id, page_id):
    """
    Fetch plain text content for a specific page.
    
    Returns just the text content, useful for reading.
    """
    content_dir = SOURCE_DIR / source_id / f'{source_id}_content'
    content_file = content_dir / f'{page_id}.json'
    
    if not content_file.exists():
        return jsonify({'error': f'Content not found: {page_id}'}), 404
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        return jsonify({
            'id': page_id,
            'title': content.get('title', ''),
            'text': content.get('text', ''),
            'chars': content.get('chars', [])
        })
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch_content', methods=['POST'])
def api_batch_content():
    """
    Fetch content for multiple pages at once.
    
    Request body (JSON):
        source: str - Source ID
        page_ids: list - List of page IDs to fetch
    
    Returns:
        JSON array of page content objects
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    source_id = data.get('source')
    page_ids = data.get('page_ids', [])
    
    if not source_id or not page_ids:
        return jsonify({'error': 'Source and page_ids are required'}), 400
    
    content_dir = SOURCE_DIR / source_id / f'{source_id}_content'
    
    if not content_dir.exists():
        return jsonify({'error': 'Content directory not found'}), 404
    
    results = []
    
    for page_id in page_ids[:50]:
        content_file = content_dir / f'{page_id}.json'
        
        if content_file.exists():
            try:
                with open(content_file, 'r', encoding='utf-8') as f:
                    results.append(json.load(f))
            except (json.JSONDecodeError, IOError):
                results.append({'id': page_id, 'error': 'Failed to load'})
    
    return jsonify({
        'source': source_id,
        'requested': len(page_ids),
        'returned': len(results),
        'pages': results
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from static/ directory."""
    return send_from_directory('static', filename)


@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve data files from data/ directory."""
    return send_from_directory('data', filename)


if __name__ == '__main__':
    print("=" * 50)
    print("Mandarin Learning Tools - Flask Server")
    print("=" * 50)
    print()
    print("Available sources:")
    sources = discover_sources()
    if sources:
        for src in sources:
            print(f"  - {src['id']}: {src['name']} ({src['pagesWithChars']} pages with chars)")
    else:
        print("  (none found - add data to source/ directory)")
    print()
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
