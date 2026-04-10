#!/usr/bin/env python3
"""
Corpus Intake Tool for Mandarin Learning Tools

Ingests text collections and creates all required companion files for the Flask API.
Automatically creates the folder structure and generates:

- <name>.json              - Full content records with characters
- <name>_data.json         - Per-record data (text_length, characters)
- <name>_inv_index.json    - Inverted index (character -> record IDs)
- <name>_freq.json         - Character frequency counts
- <name>_corpus_config.json - Metadata (name, description, stats)
- <name>.sample.json       - Small test subset (2 entries)

Usage:
    python ingest_corpus.py -i <input> -n <name> [-o <output_dir>] [-d <description>]

Input formats supported:
    - JSON array: [{"title": "...", "content": "..."}, ...]
    - JSON Lines (.jsonl): One JSON object per line
    - Directory: All .txt/.json files in directory
    - Glob pattern: Files matching pattern
    - Text file: Delimited by ---, ===, or double newlines

Examples:
    python ingest_corpus.py -i stories.json -n stories -d "Chinese stories"
    python ingest_corpus.py -i ./texts/ -n my_corpus
    python ingest_corpus.py -i "*.txt" -n corpus
    python ingest_corpus.py -i input.jsonl -n corpus -o source/
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from glob import glob as glob_glob

CHINESE_REGEX = re.compile(r'[\u4e00-\u9fff]')

DEFAULT_SAMPLE_SIZE = 2
DEFAULT_SOURCE_DIR = "source"


def extract_characters(text):
    """Extract unique Chinese characters from text using regex."""
    if not text:
        return []
    matches = CHINESE_REGEX.findall(text)
    return list(set(matches))


def parse_json_array(file_path):
    """Parse JSON array file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"JSON file must contain an array, got: {type(data)}")

    return data


def parse_json_lines(file_path):
    """Parse JSON Lines file (.jsonl)."""
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                records.append(obj)
            except json.JSONDecodeError as e:
                print(f"  Warning: Skipping line {line_num}: {e}")
    return records


def parse_text_file(file_path, delimiter=None):
    """Parse plain text file with story boundaries.
    
    Delimiter options:
        - '---': Horizontal rule
        - '===': Triple equals
        - empty: Double newline (\\n\\n)
        - 'title': Title-based (line starting story is title)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if delimiter is None:
        if '---' in content:
            delimiter = '---'
        elif '===' in content:
            delimiter = '==='
        else:
            delimiter = 'empty'

    if delimiter == 'empty':
        stories = content.split('\n\n\n')
    else:
        stories = content.split(f'\n{delimiter}\n')

    records = []
    for i, story in enumerate(stories):
        story = story.strip()
        if not story:
            continue
        lines = story.split('\n')
        first_line = lines[0].strip() if lines else ''
        rest = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ''

        if delimiter == 'title':
            title = first_line
            text = rest
        else:
            title = f"Story {i + 1}"
            text = story

        records.append({
            "title": title,
            "content": text
        })

    return records


def load_records_from_input(input_path, delimiter=None):
    """Load records from various input formats."""
    input_path = os.path.expanduser(input_path.strip())

    if os.path.isfile(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext == '.json':
            return parse_json_array(input_path)
        elif ext == '.jsonl' or ext == '.jsonlines':
            return parse_json_lines(input_path)
        elif ext == '.txt':
            return parse_text_file(input_path, delimiter)
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                first_char = f.read(1)
            if first_char == '[':
                return parse_json_array(input_path)
            elif first_char == '{':
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if 'stories' in data and isinstance(data['stories'], list):
                    return data['stories']
                elif isinstance(data, dict):
                    return [data]
            return parse_text_file(input_path, delimiter)

    elif os.path.isdir(input_path):
        patterns = ['*.txt', '*.json', '*.jsonl']
        files = []
        for pattern in patterns:
            files.extend(glob_glob(os.path.join(input_path, pattern)))
        files.sort()
        
        records = []
        for file_path in files:
            try:
                file_records = load_records_from_input(file_path, delimiter)
                records.extend(file_records)
            except Exception as e:
                print(f"  Warning: Skipping {file_path}: {e}")
        return records

    else:
        files = glob_glob(input_path)
        if not files:
            raise FileNotFoundError(f"No files found matching: {input_path}")
        
        records = []
        for file_path in files:
            try:
                file_records = load_records_from_input(file_path, delimiter)
                records.extend(file_records)
            except Exception as e:
                print(f"  Warning: Skipping {file_path}: {e}")
        return records


def normalize_record(record):
    """Normalize record to standard format {id, title, source, content, characters}."""
    title = record.get('title') or record.get('title', 'Untitled')
    content = record.get('content') or record.get('text', '')
    source = record.get('source', '')

    return {
        'title': title,
        'source': source,
        'content': content
    }


def build_index_and_freq(records):
    """Build inverted index and character frequency from records."""
    char_index = {}
    char_freq = Counter()

    for record in records:
        chars = record.get('characters', [])
        record_id = str(record.get('id', ''))
        
        for char in chars:
            if char not in char_index:
                char_index[char] = []
            if record_id not in char_index[char]:
                char_index[char].append(record_id)
            char_freq[char] += 1

    return char_index, dict(char_freq)


def build_record_data(records, char_freq):
    """Build record data (text_length and characters ordered by frequency)."""
    char_freq_sorted = sorted(char_freq.keys(), key=lambda c: char_freq[c], reverse=True)
    
    record_data = {}
    for record in records:
        record_id = str(record['id'])
        content = record.get('content', '')
        chars = record.get('characters', [])
        
        ordered_chars = sorted(chars, key=lambda c: char_freq_sorted.index(c) if c in char_freq_sorted else float('inf'))
        
        record_data[record_id] = {
            "text_length": len(content),
            "characters": ordered_chars
        }
    
    return record_data


def create_corpus_config(name, description, total_records, unique_chars):
    """Create corpus config metadata."""
    return {
        "name": name,
        "description": description,
        "totalRecords": total_records,
        "uniqueChars": unique_chars,
        "buildDate": datetime.now().isoformat()
    }


def create_source_index(name, description, total_records, unique_chars):
    """Create source-specific index.json manifest."""
    return {
        "sourceId": name,
        "name": name,
        "description": description,
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "stats": {
            "totalRecords": total_records,
            "uniqueChars": unique_chars
        },
        "files": {
            "content": f"{name}.json",
            "data": f"{name}_data.json",
            "invIndex": f"{name}_inv_index.json",
            "freq": f"{name}_freq.json",
            "config": f"{name}_corpus_config.json",
            "sample": f"{name}.sample.json"
        },
        "loadConfig": {
            "lazyLoadContent": True,
            "loadDataOnDemand": True,
            "loadIndexAlways": True
        }
    }


def save_json(data, file_path, minify=False):
    """Save data to JSON file."""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        if minify:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        else:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Corpus Intake Tool - Create source files for Mandarin learning app',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ingest_corpus.py -i input.json -n stories -d "Chinese stories"
  python ingest_corpus.py -i ./texts/ -n my_corpus
  python ingest_corpus.py -i "*.txt" -n corpus -o source/
  python ingest_corpus.py -i long_text.txt -n corpus --delimiter "---"
        """
    )
    parser.add_argument(
        '-i', '--input', '-f', '--file',
        required=True,
        help='Input: JSON file, directory, glob pattern, or text file'
    )
    parser.add_argument(
        '-n', '--name',
        required=True,
        help='Source name (used in output filenames)'
    )
    parser.add_argument(
        '-o', '--output',
        default=DEFAULT_SOURCE_DIR,
        help=f'Output directory (default: {DEFAULT_SOURCE_DIR})'
    )
    parser.add_argument(
        '-d', '--description',
        default='',
        help='Source description for metadata'
    )
    parser.add_argument(
        '--delimiter',
        choices=['---', '===', 'empty', 'title'],
        help='Text file delimiter (auto-detected if not specified)'
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        default=DEFAULT_SAMPLE_SIZE,
        help=f'Number of records for sample file (default: {DEFAULT_SAMPLE_SIZE})'
    )

    args = parser.parse_args()

    input_path = args.input
    name = args.name
    output_dir = args.output.rstrip('/').rstrip('\\')
    description = args.description or f"{name} corpus"
    delimiter = args.delimiter
    sample_size = args.sample_size

    print(f"Corpus Intake Tool")
    print(f"=" * 40)
    print(f"Input:    {input_path}")
    print(f"Name:     {name}")
    print(f"Output:   {output_dir}/{name}/")
    print(f"Description: {description}")
    print()

    print("Loading records...")
    raw_records = load_records_from_input(input_path, delimiter)
    print(f"  Loaded {len(raw_records)} raw records")

    print("Normalizing records...")
    records = []
    seen_content = set()
    next_id = 1

    for raw in raw_records:
        normalized = normalize_record(raw)
        content = normalized.get('content', '')
        
        if not content:
            continue
        
        if content in seen_content:
            print(f"  Skipping duplicate: {normalized.get('title', 'Untitled')}")
            continue
        seen_content.add(content)

        chars = extract_characters(content)
        
        records.append({
            "id": next_id,
            "title": normalized['title'],
            "source": normalized['source'],
            "content": content,
            "characters": chars
        })
        next_id += 1

    print(f"  {len(records)} unique records after deduplication")
    print(f"  Extracting characters...")

    unique_chars = set()
    for record in records:
        unique_chars.update(record.get('characters', []))
    print(f"  Found {len(unique_chars)} unique Chinese characters")

    print("Building index...")
    char_index, char_freq = build_index_and_freq(records)

    print("Building record data...")
    record_data = build_record_data(records, char_freq)

    source_dir = os.path.join(output_dir, name)
    print(f"Creating output directory: {source_dir}/")

    print("Saving files...")
    content_file = os.path.join(source_dir, f"{name}.json")
    save_json(records, content_file)
    print(f"  Saved: {content_file}")

    data_file = os.path.join(source_dir, f"{name}_data.json")
    save_json(record_data, data_file, minify=True)
    print(f"  Saved: {data_file}")

    inv_index_file = os.path.join(source_dir, f"{name}_inv_index.json")
    save_json({"index": char_index}, inv_index_file, minify=True)
    print(f"  Saved: {inv_index_file}")

    freq_file = os.path.join(source_dir, f"{name}_freq.json")
    save_json(char_freq, freq_file, minify=True)
    print(f"  Saved: {freq_file}")

    config = create_corpus_config(name, description, len(records), len(unique_chars))
    config_file = os.path.join(source_dir, f"{name}_corpus_config.json")
    save_json(config, config_file)
    print(f"  Saved: {config_file}")

    sample_schema = [
        {
            "id": 1,
            "title": "Example Title",
            "source": "example",
            "content": "这是示例内容，包含中文字符。",
            "characters": ["这", "是", "示", "例", "内", "容", "包", "含", "中", "文", "字", "符"]
        },
        {
            "id": 2,
            "title": "第二个示例",
            "source": "example",
            "content": "另一个示例文本用于展示数据结构。",
            "characters": ["另", "一", "个", "示", "例", "文", "本", "用", "于", "展", "示", "数", "据", "结", "构"]
        }
    ]
    sample_file = os.path.join(source_dir, f"{name}.sample.json")
    save_json(sample_schema, sample_file)
    print(f"  Saved: {sample_file}")

    source_index = create_source_index(name, description, len(records), len(unique_chars))
    index_file = os.path.join(source_dir, f"{name}_index.json")
    save_json(source_index, index_file)
    print(f"  Saved: {index_file}")

    print()
    print("=" * 40)
    print("Complete!")
    print(f"  Total records: {len(records)}")
    print(f"  Unique chars: {len(unique_chars)}")
    print(f"  Output dir: {source_dir}")


if __name__ == '__main__':
    main()