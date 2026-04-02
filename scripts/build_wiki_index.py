#!/usr/bin/env python3
"""
Wikipedia Index Builder for Mandarin Learning Tools

Downloads and processes the Chinese Wikipedia dump to create an inverted index
that maps Chinese characters to the Wikipedia pages that contain them.

Supports multiple input formats:
- XML bz2: Standard Wikipedia XML dump (zhwiki-*-pages-articles.xml.bz2)
- ZIM: Kiwix offline Wikipedia format

Usage:
    python build_wiki_index.py [--download] [--input INPUT_FILE]

Options:
    --download     Download the latest Wikipedia dump (XML bz2 format)
    --input FILE   Use a local Wikipedia dump file (XML bz2 or ZIM)

Requirements:
    For XML bz2: Standard library only (no extra dependencies)
    For ZIM: Either:
        - libzim Python bindings: pip install libzim
        - zimdump CLI tool: Available in zim-tools package
"""

import argparse
import bz2
import json
import os
import re
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

INDEX_FILENAME = "data/wiki_index.json"
CHINESE_REGEX = re.compile(r'[\u4e00-\u9fff]')

WIKI_DUMP_URL = "https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2"
DUMP_FILENAME = "zhwiki-latest-pages-articles.xml.bz2"


def download_wikipedia_dump():
    """Download the Chinese Wikipedia dump (XML bz2 format)."""
    print(f"Downloading Chinese Wikipedia dump from {WIKI_DUMP_URL}")
    print("This may take a while (several GB)...")
    print("For ZIM files, download manually from https://download.kiwix.org/zim/wikipedia/")

    try:
        urlretrieve(WIKI_DUMP_URL, DUMP_FILENAME)
        print(f"Download complete: {DUMP_FILENAME}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def extract_plain_text(content):
    """
    Extract plain text from Wikipedia content.
    Handles both wiki markup (for XML) and HTML (for ZIM).
    """
    text = content

    if not text:
        return ""

    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref[^>]*/>', '', text)

    text = re.sub(r'<gallery>.*?</gallery>', '', text, flags=re.DOTALL)

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

    text = re.sub(r'<[^>]+>', '', text)

    text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)

    text = re.sub(r"={2,}\s*([^=]+)\s*={2,}", r'\1', text)

    text = re.sub(r'^[*#]+', '', text, flags=re.MULTILINE)

    text = re.sub(r'^----+', '', text, flags=re.MULTILINE)

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def extract_characters(text):
    """Extract unique Chinese characters from text."""
    return list(set(CHINESE_REGEX.findall(text)))


def check_zim_tools():
    """Check if zimdump command-line tool is available."""
    try:
        result = subprocess.run(
            ['zimdump', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return False


def try_import_libzim():
    """Try to import libzim Python bindings."""
    try:
        import libzim
        return True
    except ImportError:
        return False


def process_zim_with_libzim(input_file):
    """Process ZIM file using libzim Python bindings."""
    import libzim

    print(f"Processing ZIM file with libzim: {input_file}")

    reader = libzim.Library(input_file).allbooks()
    searcher = libzim.Searcher(libzim.Library(input_file))
    
    pages = {}
    char_index = {}
    total_pages = 0
    pages_with_chars = 0
    progress_interval = 1000

    for entry in reader.iter():
        total_pages += 1

        if total_pages % progress_interval == 0:
            print(f"  Processed {total_pages} pages...")

        try:
            article = entry.get_article()
            title = article.title
            content = article.content

            if not title or not content:
                continue

            plain_text = extract_plain_text(content)
            chars = extract_characters(plain_text)

            if chars:
                pages_with_chars += 1
                page_id = str(total_pages)

                pages[page_id] = {
                    'title': title,
                    'chars': chars
                }

                for char in chars:
                    if char not in char_index:
                        char_index[char] = []
                    char_index[char].append(page_id)

        except Exception as e:
            continue

    return {
        'version': '1.0',
        'buildDate': datetime.now().isoformat(),
        'totalPages': total_pages,
        'pagesWithChars': pages_with_chars,
        'uniqueChars': len(char_index),
        'pages': pages,
        'index': char_index
    }


def process_zim_with_zimdump(input_file):
    """Process ZIM file using zimdump command-line tool."""
    print(f"Processing ZIM file with zimdump: {input_file}")

    pages = {}
    char_index = {}
    total_pages = 0
    pages_with_chars = 0
    progress_interval = 1000

    cmd = ['zimdump', 'dump', '--dir', input_file]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"zimdump error: {result.stderr}")
            return None

        lines = result.stdout.split('\n')
        current_title = None
        current_content = []

        for line in lines:
            if line.startswith('M/'):
                if current_title:
                    plain_text = extract_plain_text(''.join(current_content))
                    chars = extract_characters(plain_text)

                    if chars:
                        pages_with_chars += 1
                        page_id = str(total_pages)

                        pages[page_id] = {
                            'title': current_title,
                            'chars': chars
                        }

                        for char in chars:
                            if char not in char_index:
                                char_index[char] = []
                            char_index[char].append(page_id)

                total_pages += 1
                if total_pages % progress_interval == 0:
                    print(f"  Processed {total_pages} pages...")

                current_title = line[2:].strip()
                current_content = []

            elif current_title and line.strip():
                current_content.append(line)

        if current_title:
            plain_text = extract_plain_text(''.join(current_content))
            chars = extract_characters(plain_text)

            if chars:
                pages_with_chars += 1
                page_id = str(total_pages)

                pages[page_id] = {
                    'title': current_title,
                    'chars': chars
                }

                for char in chars:
                    if char not in char_index:
                        char_index[char] = []
                    char_index[char].append(page_id)

    except subprocess.TimeoutExpired:
        print("zimdump timed out")
        return None
    except Exception as e:
        print(f"Error running zimdump: {e}")
        return None

    return {
        'version': '1.0',
        'buildDate': datetime.now().isoformat(),
        'totalPages': total_pages,
        'pagesWithChars': pages_with_chars,
        'uniqueChars': len(char_index),
        'pages': pages,
        'index': char_index
    }


def process_zim_file(input_file):
    """Process ZIM file using available tools."""
    has_libzim = try_import_libzim()
    has_zimdump = check_zim_tools()

    if has_libzim:
        return process_zim_with_libzim(input_file)
    elif has_zimdump:
        return process_zim_with_zimdump(input_file)
    else:
        print("\n" + "="*60)
        print("ERROR: Cannot process ZIM file - no ZIM library found")
        print("="*60)
        print("\nPlease install one of the following:")
        print()
        print("Option 1: Install libzim Python bindings")
        print("  pip install libzim")
        print("  (May require compilation tools)")
        print()
        print("Option 2: Install zim-tools (includes zimdump)")
        print("  Ubuntu/Debian: sudo apt install zim-tools")
        print("  macOS: brew install zim-tools")
        print("  Windows: Download from https://github.com/kiwix/kiwix-tools/releases")
        print()
        print("Option 3: Use XML bz2 format instead")
        print(f"  Download from: {WIKI_DUMP_URL}")
        print("  Run: python build_wiki_index.py --download")
        print("="*60)
        return None


def process_wikipedia_xml(input_file):
    """Process Wikipedia XML dump (plain or bz2 compressed)."""
    print(f"Processing Wikipedia XML dump: {input_file}")

    pages = {}
    char_index = {}

    total_pages = 0
    pages_with_chars = 0
    progress_interval = 10000

    if input_file.endswith('.bz2'):
        opener = bz2.open
    else:
        opener = open

    with opener(input_file, 'rt', encoding='utf-8') as f:
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

                    if page_id and page_title:
                        combined_content = '\n'.join(page_content)

                        if combined_content.startswith('#REDIRECT'):
                            continue

                        plain_text = extract_plain_text(combined_content)
                        chars = extract_characters(plain_text)

                        if chars:
                            pages_with_chars += 1

                            pages[page_id] = {
                                'title': page_title,
                                'chars': chars
                            }

                            for char in chars:
                                if char not in char_index:
                                    char_index[char] = []
                                char_index[char].append(page_id)

    print(f"Processing complete!")
    print(f"  Total pages: {total_pages}")
    print(f"  Pages with Chinese characters: {pages_with_chars}")
    print(f"  Unique characters: {len(char_index)}")

    return {
        'version': '1.0',
        'buildDate': datetime.now().isoformat(),
        'totalPages': total_pages,
        'pagesWithChars': pages_with_chars,
        'uniqueChars': len(char_index),
        'pages': pages,
        'index': char_index
    }


def process_file(input_file):
    """Process file based on its extension."""
    input_file = input_file.strip()

    if input_file.endswith('.zim'):
        return process_zim_file(input_file)
    elif input_file.endswith('.xml.bz2') or input_file.endswith('.xml'):
        return process_wikipedia_xml(input_file)
    else:
        print(f"Unknown file format: {input_file}")
        print("Supported formats: .xml.bz2, .xml, .zim")
        return None


def save_index(index, output_file):
    """Save the index to a JSON file."""
    print(f"Saving index to {output_file}")

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))

    file_size = os.path.getsize(output_file)
    print(f"Index saved! File size: {file_size / (1024*1024):.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='Build Wikipedia inverted index for Mandarin learning tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download and process XML bz2 dump
  python build_wiki_index.py --download

  # Process local XML dump
  python build_wiki_index.py --input wikipedia_zhwiki.xml.bz2

  # Process ZIM file (requires zim-tools or libzim)
  python build_wiki_index.py --input wikipedia_zh_all_maxi.zim

Supported input formats:
  - XML bz2: Standard Wikipedia XML dump
  - XML: Uncompressed Wikipedia XML dump
  - ZIM: Kiwix offline Wikipedia format
        """
    )
    parser.add_argument(
        '--download', '-d',
        action='store_true',
        help='Download the latest Wikipedia XML dump before processing'
    )
    parser.add_argument(
        '--input', '-i',
        help='Path to local Wikipedia dump file (XML bz2, XML, or ZIM)'
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
                print("\nError: Could not download Wikipedia dump.")
                print(f"Please download manually from: {WIKI_DUMP_URL}")
                print("\nFor ZIM files, download from: https://download.kiwix.org/zim/wikipedia/")
                print("Then run with: python build_wiki_index.py --input <path_to_file>")
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

    index = process_file(input_file)

    if index is None:
        sys.exit(1)

    print(f"\nSummary:")
    print(f"  Total pages: {index['totalPages']}")
    print(f"  Pages with Chinese: {index['pagesWithChars']}")
    print(f"  Unique characters: {index['uniqueChars']}")

    save_index(index, args.output)

    print("\nDone! Copy the index file to your web app's data folder:")
    print(f"  {args.output}")
    print("\nThen use it with wiki_curriculum_builder.html")


if __name__ == '__main__':
    main()
