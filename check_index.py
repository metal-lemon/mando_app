import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open('source/storyCollection/storyCollection_inv_index.json', 'r', encoding='utf-8'))
idx = d.get('index', {})

# Get keys
keys = list(idx.keys())
print('Total chars in index:', len(keys))
print('First 10 keys:', keys[:10])

# Check for character by ordinal
test_codes = [0x96ea, 0x718a, 0x5c0f]  # 雪, 熊, 小
for code in test_codes:
    char = chr(code)
    in_idx = char in idx
    print(f'U+{code:04X} ({char}): {in_idx}')