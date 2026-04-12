import json
import urllib.request
import urllib.parse

data = json.dumps({
    "source": "storyCollection",
    "targetChars": ["雪", "小", "熊"],
    "knownChars": ["小", "白", "兔"]
}).encode('utf-8')

req = urllib.request.Request(
    'http://localhost:5000/api/build-pool',
    data=data,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Status:", response.status)
        print("Pool size:", result.get('poolSize'))
        print("Coverage:", f"{result.get('coverage')*100:.1f}%")
        print("Thresholds:", result.get('thresholds'))
        print("Covered targets:", result.get('coveredTargets'), "/", result.get('totalTargets'))
except Exception as e:
    print("Error:", e)