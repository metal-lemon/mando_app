#!/usr/bin/env python3
"""
Wikipedia Index Builder for Mandarin Learning Tools

Downloads and processes the Chinese Wikipedia dump to create an inverted index
that maps Chinese characters to the Wikipedia pages that contain them.

Usage:
    python build_wiki_index.py [--download] [--input INPUT_FILE]

Options:
    --download     Download the latest Wikipedia dump before processing
    --input FILE   Use a local Wikipedia XML dump file
"""

import argparse
import bz2
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

# Wikipedia dump URL
WIKI_DUMP_URL = "https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2"
DUMP_FILENAME = "zhwiki-latest-pages-articles.xml.bz2"
INDEX_FILENAME = "data/wiki_index.json"

# Chinese character regex
CHINESE_REGEX = re.compile(r'[\u4e00-\u9fff]')


def download_wikipedia_dump():
    """Download the Chinese Wikipedia dump."""
    print(f"Downloading Chinese Wikipedia dump from {WIKI_DUMP_URL}")
    print("This may take a while (several GB)...")

    try:
        urlretrieve(WIKI_DUMP_URL, DUMP_FILENAME)
        print(f"Download complete: {DUMP_FILENAME}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def extract_plain_text(xml_content):
    """
    Extract plain text from Wikipedia XML content.
    Removes wiki markup, templates, and HTML tags.
    """
    text = xml_content

    # Remove comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Remove <ref>...</ref> tags (references)
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref[^>]*/>', '', text)

    # Remove <gallery>...</gallery>
    text = re.sub(r'<gallery>.*?</gallery>', '', text, flags=re.DOTALL)

    # Remove templates {{...}}
    depth = 0
    result = []
    i = 0
    while i < len(text):
        if text[i:i+2] == '{{':
            depth += 1
            i += 2
        elif text[i:i+2] == '}}' and depth > 0:
            depth -= 1
            i += 2
        elif depth == 0:
            result.append(text[i])
            i += 1
        else:
            i += 1
    text = ''.join(result)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove wiki links [[...]]
    text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)

    # Remove wiki headings ===...===
    text = re.sub(r"={2,}\s*([^=]+)\s*={2,}", r'\1', text)

    # Remove wiki lists
    text = re.sub(r'^[*#]+', '', text, flags=re.MULTILINE)

    # Remove wiki horizontal rules
    text = re.sub(r'^----+', '', text, flags=re.MULTILINE)

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def extract_characters(text):
    """Extract unique Chinese characters from text."""
    return list(set(CHINESE_REGEX.findall(text)))


def process_wikipedia_dump(input_file):
    """
    Process the Wikipedia XML dump and build inverted index.

    Returns a dictionary with:
    - version: index format version
    - buildDate: when the index was built
    - totalPages: number of pages processed
    - uniqueChars: number of unique characters found
    - pages: dict mapping page_id -> {title, chars}
    - index: dict mapping char -> [page_ids]
    """
    print(f"Processing Wikipedia dump: {input_file}")

    pages = {}
    char_index = {}

    total_pages = 0
    pages_with_chars = 0
    progress_interval = 10000

    # Determine if file is bz2 compressed
    if input_file.endswith('.bz2'):
        opener = bz2.open
    else:
        opener = open

    with opener(input_file, 'rt', encoding='utf-8') as f:
        # Parse XML incrementally using iterparse
        page_id = None
        page_title = None
        page_content = []
        in_page = False
        in_revision = False
        in_text = False

        for event, elem in ET.iterparse(f, events=['start', 'end']):
            tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

            if event == 'start':
                if tag_name == 'page':
                    in_page = True
                    page_id = None
                    page_title = None
                    page_content = []
                elif tag_name == 'revision' and in_page:
                    in_revision = True
                elif tag_name == 'text' and in_revision:
                    in_text = True

            elif event == 'end':
                if tag_name == 'title' and in_page:
                    page_title = elem.text or ''
                elif tag_name == 'id' and in_page and page_id is None:
                    page_id = elem.text or ''
                elif tag_name == 'text' and in_text:
                    if elem.text:
                        page_content.append(elem.text)
                    in_text = False
                elif tag_name == 'revision' and in_page:
                    in_revision = False
                elif tag_name == 'page' and in_page:
                    in_page = False

                    total_pages += 1

                    if total_pages % progress_interval == 0:
                        print(f"  Processed {total_pages} pages...")

                    # Only process main namespace pages with content
                    if page_id and page_title:
                        combined_content = '\n'.join(page_content)

                        # Skip redirects and disambiguation pages
                        if combined_content.startswith('#REDIRECT'):
                            continue

                        chars = extract_characters(combined_content)

                        if chars:
                            pages_with_chars += 1

                            # Store page data
                            pages[page_id] = {
                                'title': page_title,
                                'chars': chars
                            }

                            # Update inverted index
                            for char in chars:
                                if char not in char_index:
                                    char_index[char] = []
                                char_index[char].append(page_id)

    print(f"Processing complete!")
    print(f"  Total pages: {total_pages}")
    print(f"  Pages with Chinese characters: {pages_with_chars}")
    print(f"  Unique characters: {len(char_index)}")

    # Build final index structure
    index = {
        'version': '1.0',
        'buildDate': datetime.now().isoformat(),
        'totalPages': total_pages,
        'pagesWithChars': pages_with_chars,
        'uniqueChars': len(char_index),
        'pages': pages,
        'index': char_index
    }

    return index


def save_index(index, output_file):
    """Save the index to a JSON file."""
    print(f"Saving index to {output_file}")

    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))

    # Calculate file size
    file_size = os.path.getsize(output_file)
    print(f"Index saved! File size: {file_size / (1024*1024):.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='Build Wikipedia inverted index for Mandarin learning tools'
    )
    parser.add_argument(
        '--download', '-d',
        action='store_true',
        help='Download the latest Wikipedia dump before processing'
    )
    parser.add_argument(
        '--input', '-i',
        help='Path to local Wikipedia XML dump file (overrides download)'
    )
    parser.add_argument(
        '--output', '-o',
        default=INDEX_FILENAME,
        help=f'Output index file path (default: {INDEX_FILENAME})'
    )

    args = parser.parse_args()

    input_file = args.input

    if not input_file:
        if args.download or not os.path.exists(DUMP_FILENAME):
            if not download_wikipedia_dump():
                print("Error: Could not download Wikipedia dump.")
                print(f"Please download manually from: {WIKI_DUMP_URL}")
                print("Then run with: python build_wiki_index.py --input <path_to_dump>")
                sys.exit(1)
            input_file = DUMP_FILENAME
        else:
            print(f"Using existing file: {DUMP_FILENAME}")
            input_file = DUMP_FILENAME

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    print(f"\nInput file: {input_file}")
    print(f"Output file: {args.output}")
    print()

    # Process the dump
    index = process_wikipedia_dump(input_file)

    # Save the index
    save_index(index, args.output)

    print("\nDone! Copy the index file to your web app's data folder:")
    print(f"  {args.output}")
    print("\nThen use it with wiki_curriculum_builder.html")


if __name__ == '__main__':
    main()
