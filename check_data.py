import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Check data file - try integer key
d = json.load(open('source/storyCollection/storyCollection_data.json', 'r', encoding='utf-8'))
print('Total records in data:', len(d))

# Keys might be strings or integers
sample_keys = list(d.keys())[:3]
print('Sample keys:', sample_keys)
print('Key types:', [type(k) for k in sample_keys])

# Try both string and int keys
rec1 = d.get('1') or d.get(1)
print('Record 1:', rec1)

# Check content file
c = json.load(open('source/storyCollection/storyCollection.json', 'r', encoding='utf-8'))
print('Total records in content:', len(c))
if c:
    print('First record id:', c[0].get('id'))
    print('First record title:', c[0].get('title')[:20] if c[0].get('title') else 'None')