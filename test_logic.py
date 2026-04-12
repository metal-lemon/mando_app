import json

d = json.load(open('source/storyCollection/storyCollection_inv_index.json', 'r', encoding='utf-8'))
index = d.get('index', {})

target_chars = {'雪', '熊', '小'}
known_chars = set()

page_coverage = {}
for char in target_chars:
    posting_list = index.get(char, [])
    for page_id in posting_list:
        if page_id not in page_coverage:
            page_coverage[page_id] = set()
        page_coverage[page_id].add(char)

data = json.load(open('source/storyCollection/storyCollection_data.json', 'r', encoding='utf-8'))

# Check efficiency for records passing step 1
alpha = 30.0
theta = 0.3

records_checked = []
for page_id, matched_chars in page_coverage.items():
    chars = data.get(str(page_id), {}).get('characters', [])
    if not chars:
        continue
    
    unique_chars = list(set(chars))
    
    # Step 1
    limit = len(known_chars) + (alpha * 3)
    if len(unique_chars) > limit:
        continue
    
    # Step 2
    unknown_in_record = [c for c in unique_chars if c not in known_chars]
    target_in_record = [c for c in unknown_in_record if c in target_chars]
    nontarget_in_record = [c for c in unknown_in_record if c not in target_chars]
    
    if len(target_in_record) == 0:
        continue
    
    # Step 3 efficiency
    efficiency = len(target_in_record) / (len(target_in_record) + len(nontarget_in_record))
    records_checked.append((page_id, len(target_in_record), len(nontarget_in_record), efficiency))

print(f"Records passing steps 1-2: {len(records_checked)}")
print("Efficiencies:")
for pid, tgt, nt, eff in records_checked:
    print(f"  ID: {pid}, targets: {tgt}, non-targets: {nt}, efficiency: {eff:.4f}")