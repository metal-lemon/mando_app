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
import sys
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, Response


def _ensure_jieba():
    """Ensure jieba is installed, auto-install if missing."""
    try:
        import jieba
        return jieba
    except ImportError:
        print("Installing jieba...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'jieba'])
        import jieba
        return jieba

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR / 'source'
DATA_DIR = BASE_DIR / 'data'


def discover_sources():
    """Discover sources using index.json manifests in each source folder."""
    sources = []
    
    if not SOURCE_DIR.exists():
        return sources
    
    for source_path in SOURCE_DIR.iterdir():
        if not source_path.is_dir():
            continue
        
        source_id = source_path.name
        index_file = source_path / f'{source_id}_index.json'
        
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
                
                files = index.get('files', {})
                file_status = {}
                for key, filename in files.items():
                    file_status[key] = (source_path / filename).exists()
                
                stats = index.get('stats', {})
                sources.append({
                    'id': source_id,
                    'name': index.get('name', source_id),
                    'description': index.get('description', ''),
                    'totalRecords': stats.get('totalRecords', 0),
                    'uniqueChars': stats.get('uniqueChars', 0),
                    'files': file_status,
                    'hasIndex': file_status.get('invIndex', False),
                    'hasData': file_status.get('data', False),
                    'hasContent': file_status.get('content', False)
                })
            except (json.JSONDecodeError, IOError):
                sources.append(_fallback_source(source_id))
        else:
            sources.append(_fallback_source(source_id))
    
    return sources


def _fallback_source(source_id):
    """Create fallback source entry when no config is found."""
    return {
        'id': source_id,
        'name': source_id.title(),
        'description': 'No configuration found',
        'totalRecords': 0,
        'uniqueChars': 0,
        'buildDate': '',
        'hasContent': False,
        'hasData': False,
        'hasIndex': False,
        'hasFreq': False,
        'hasConfig': False,
        'isValid': False
    }


def load_source_index(source_id):
    """Load the inverted index for a source."""
    source_path = SOURCE_DIR / source_id
    data_file = source_path / f'{source_id}_inv_index.json'
    
    if not data_file.exists():
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_source_index_manifest(source_id):
    """Load source index.json for metadata."""
    index_file = SOURCE_DIR / source_id / f'{source_id}_index.json'
    if not index_file.exists():
        return None
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_source_data(source_id):
    """Load lightweight _data.json for a source."""
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


@app.route('/api/source/<source_id>/meta', methods=['GET'])
def api_source_meta(source_id):
    """Get source metadata and file availability."""
    index = load_source_index_manifest(source_id)
    if not index:
        return jsonify({'error': 'Source not found'}), 404
    
    source_path = SOURCE_DIR / source_id
    files = index.get('files', {})
    file_status = {k: (source_path / v).exists() for k, v in files.items()}
    
    return jsonify({
        'sourceId': source_id,
        'name': index.get('name'),
        'description': index.get('description'),
        'stats': index.get('stats', {}),
        'files': file_status,
        'ready': file_status.get('invIndex', False) and file_status.get('data', False)
    })


@app.route('/api/source/<source_id>/data', methods=['GET'])
def api_source_data(source_id):
    """Get lightweight per-record data without full content."""
    data = load_source_data(source_id)
    if data is None:
        return jsonify({'error': 'Source data not found'}), 404
    return jsonify({
        'sourceId': source_id,
        'records': data,
        'count': len(data)
    })


@app.route('/api/backup', methods=['GET'])
def api_get_backup():
    """Get server backup of characters."""
    backup_file = DATA_DIR / 'my_characters.json'
    if not backup_file.exists():
        return jsonify({'characters': [], 'count': 0})
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except (json.JSONDecodeError, IOError):
        return jsonify({'characters': [], 'count': 0})


@app.route('/api/backup', methods=['POST'])
def api_save_backup():
    """Save characters to server backup (overwrites)."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    backup_file = DATA_DIR / 'my_characters.json'
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True, 'count': data.get('count', 0)})
    except IOError as e:
        return jsonify({'error': f'Failed to save: {str(e)}'}), 500


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


@app.route('/api/build-pool', methods=['POST'])
def api_build_pool():
    """
    Build a candidate pool by applying steps 1-3 server-side.
    This avoids sending millions of records to the client.
    
    Request body (JSON):
        source: str - Source ID
        targetChars: list - Characters to learn
        knownChars: list - Characters already known
        maxPoolSize: int - Maximum candidates to return (default 100)
    
    Returns:
        JSON with filtered pool and metadata
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    source_id = data.get('source')
    target_chars = set(data.get('targetChars', []))
    known_chars = set(data.get('knownChars', []))
    max_pool_size = min(int(data.get('maxPoolSize', 100)), 200)
    
    if not source_id:
        return jsonify({'error': 'Source is required'}), 400
    
    if not target_chars:
        return jsonify({'error': 'Target characters are required'}), 400
    
    index_data = load_source_index(source_id)
    if not index_data:
        return jsonify({'error': f'Source not found: {source_id}'}), 404
    
    index = index_data.get('index', {})
    total_targets = len(target_chars)
    
    # Find records containing target characters
    page_coverage = {}
    for char in target_chars:
        posting_list = index.get(char, [])
        for page_id in posting_list:
            if page_id not in page_coverage:
                page_coverage[page_id] = set()
            page_coverage[page_id].add(char)
    
    # Load page metadata from data file
    source_path = SOURCE_DIR / source_id
    data_file = source_path / f'{source_id}_data.json'
    page_data = {}
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
    
    # Dynamic threshold parameters
    # For long-form content (stories with 150-400 unique chars), efficiency thresholds
    # are too strict. We use very permissive thresholds and let beam search optimize.
    alpha = 50.0  # Allow longer stories initially
    theta = 0.0    # No efficiency filter - all records with targets are candidates
    max_alpha = 200.0
    min_theta = 0.0
    theta_step = 0.1
    
    pool = []
    thresholds_used = {'alpha': alpha, 'theta': theta}
    
    # Try progressively relaxed thresholds until we get candidates
    while len(pool) == 0 and alpha <= max_alpha and theta >= min_theta:
        for page_id, matched_chars in page_coverage.items():
            chars = page_data.get(page_id, {}).get('characters', [])
            if not chars:
                # Fallback: try to get from content file
                content_file = source_path / f'{source_id}.json'
                if content_file.exists():
                    try:
                        with open(content_file, 'r', encoding='utf-8') as f:
                            all_records = json.load(f)
                            for rec in all_records:
                                if str(rec.get('id')) == str(page_id) or rec.get('id') == int(page_id):
                                    chars = rec.get('characters', [])
                                    break
                    except:
                        pass
            
            unique_chars = list(set(chars))
            
            # Step 1: Numerical Cut-off
            limit = len(known_chars) + (alpha * total_targets)
            if len(unique_chars) > limit:
                continue
            
            # Step 2: Pre-split by Known Set
            known_in_record = [c for c in unique_chars if c in known_chars]
            unknown_in_record = [c for c in unique_chars if c not in known_chars]
            target_in_record = [c for c in unknown_in_record if c in target_chars]
            nontarget_in_record = [c for c in unknown_in_record if c not in target_chars]
            
            # Step 3: Efficiency-Threshold
            if len(nontarget_in_record) + len(target_in_record) == 0:
                continue
            efficiency = len(target_in_record) / (len(target_in_record) + len(nontarget_in_record))
            if efficiency < theta:
                continue
            
            pool.append({
                'id': page_id,
                'matched_chars': list(matched_chars),
                'uniqueChars': unique_chars,
                'targetChars': target_in_record,
                'nontargetChars': nontarget_in_record,
                'efficiency': efficiency
            })
            
            if len(pool) >= max_pool_size:
                break
        
        if len(pool) == 0:
            alpha += 0.5
            theta = max(min_theta, theta - theta_step)
            thresholds_used = {'alpha': alpha, 'theta': theta}
    
    # Calculate coverage
    covered_targets = set()
    for item in pool:
        for c in item['targetChars']:
            covered_targets.add(c)
    coverage = len(covered_targets) / total_targets if total_targets > 0 else 0
    
    # Load titles from content
    content_file = source_path / f'{source_id}.json'
    titles = {}
    if content_file.exists():
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                for rec in json.load(f):
                    titles[str(rec.get('id'))] = rec.get('title', 'Untitled')
        except:
            pass
    
    # Add titles to pool
    for item in pool:
        item['title'] = titles.get(str(item['id']), 'Untitled')
        # Don't include full content in response - client can fetch on demand
    
    return jsonify({
        'source': source_id,
        'pool': pool,
        'poolSize': len(pool),
        'thresholds': thresholds_used,
        'coverage': coverage,
        'totalTargets': total_targets,
        'coveredTargets': len(covered_targets)
    })


@app.route('/api/learnable-words', methods=['POST'])
def api_learnable_words():
    """
    Find dictionary words that can be formed from known characters.
    
    Request body (JSON):
        chars: list - List of known characters
    
    Returns:
        JSON with count and word list of learnable words
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    known_chars = set(data.get('chars', []))
    
    if not known_chars:
        return jsonify({'count': 0, 'words': []})
    
    dictionary_file = DATA_DIR / 'dictionary.json'
    
    if not dictionary_file.exists():
        return jsonify({'error': 'Dictionary not found'}), 404
    
    try:
        with open(dictionary_file, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'Failed to load dictionary: {str(e)}'}), 500
    
    learnable = []
    for word in dictionary:
        word_chars = word.get('chars', [])
        # Only multi-character words where ALL chars are known
        if len(word_chars) > 1 and all(ch in known_chars for ch in word_chars):
            learnable.append(word)
    
    return jsonify({
        'count': len(learnable),
        'words': learnable
    })


@app.route('/api/segment', methods=['POST'])
def api_segment():
    """
    Segment Chinese text using jieba.
    
    Request body (JSON):
        text: string - Chinese text to segment
        mode: string - 'accurate' (default), 'full', or 'search'
    
    Returns:
        JSON with word list
    """
    jieba = _ensure_jieba()
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    text = data.get('text', '')
    mode = data.get('mode', 'accurate')
    
    if not text:
        return jsonify({'words': []})
    
    if mode == 'search':
        words = jieba.cut_for_search(text)
    elif mode == 'full':
        words = jieba.cut(text, cut_all=True)
    else:
        words = jieba.cut(text)
    
    return jsonify({'words': list(words)})


@app.route('/api/content/<source_id>/<record_id>')
def api_content(source_id, record_id):
    """
    Fetch content for a specific record.
    
    Returns the content from <source>.json file.
    """
    source_path = SOURCE_DIR / source_id
    content_file = source_path / f'{source_id}.json'
    
    if not content_file.exists():
        return jsonify({'error': f'Content file not found for source: {source_id}', 'file': str(content_file)}), 404
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        # Find the specific record by ID
        if isinstance(content_data, list):
            for record in content_data:
                if str(record.get('id')) == str(record_id):
                    return jsonify(record)
            # Debug: Return first few IDs to help diagnose
            available_ids = [str(r.get('id')) for r in content_data[:10]]
            return jsonify({
                'error': f'Record not found: {record_id}',
                'requested_source': source_id,
                'file': str(content_file),
                'first_10_ids': available_ids
            }), 404
        else:
            return jsonify({'error': 'Invalid content format'}), 500
            
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/content/<source_id>/<record_id>/text')
def api_content_text(source_id, record_id):
    """
    Fetch plain text content for a specific record.
    
    Returns just the text content, useful for reading.
    """
    source_path = SOURCE_DIR / source_id
    content_file = source_path / f'{source_id}.json'
    
    if not content_file.exists():
        return jsonify({'error': f'Content file not found for source: {source_id}'}), 404
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        # Find the specific record by ID
        if isinstance(content_data, list):
            for record in content_data:
                if str(record.get('id')) == str(record_id):
                    return jsonify({
                        'id': record_id,
                        'title': record.get('title', ''),
                        'text': record.get('content', record.get('text', '')),
                        'chars': record.get('characters', record.get('chars', []))
                    })
            return jsonify({'error': f'Record not found: {record_id}'}), 404
        else:
            return jsonify({'error': 'Invalid content format'}), 500
            
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch_content', methods=['POST'])
def api_batch_content():
    """
    Fetch content for multiple records at once.
    
    Request body (JSON):
        source: str - Source ID
        record_ids: list - List of record IDs to fetch
    
    Returns:
        JSON array of content objects
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    source_id = data.get('source')
    record_ids = data.get('record_ids', [])
    
    if not source_id or not record_ids:
        return jsonify({'error': 'Source and record_ids are required'}), 400
    
    source_path = SOURCE_DIR / source_id
    content_file = source_path / f'{source_id}.json'
    
    if not content_file.exists():
        return jsonify({'error': f'Content file not found for source: {source_id}'}), 404
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        results = []
        
        if isinstance(content_data, list):
            record_id_set = set(str(rid) for rid in record_ids[:50])
            for record in content_data:
                if str(record.get('id')) in record_id_set:
                    results.append(record)
        
        return jsonify({
            'source': source_id,
            'requested': len(record_ids),
            'returned': len(results),
            'records': results
        })
        
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': str(e)}), 500


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
            content_status = "[OK]" if src.get('hasContent') else "[MISSING]"
            print(f"  - {src['id']}: {src['name']} ({src['totalRecords']} records, {src['uniqueChars']} chars) {content_status}")
    else:
        print("  (none found - add data to source/ directory)")
    print()
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
