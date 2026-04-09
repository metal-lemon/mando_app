# Mandarin Learning Tools

A web application for learning Chinese characters through structured reading paths.

## Prerequisites

- Python 3.x

## Setup

### 1. Navigate to the project folder

```powershell
cd "PATH_TO_CLONED_REPO"
```

Replace `PATH_TO_CLONED_REPO` with the actual path where you cloned the repository.

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Build Source Data

```powershell
python scripts/ingest_corpus.py -i data/stories.json -n stories -d "Chinese stories"
```

This creates files in the `source/stories/` folder.

### 4. Start the App

```powershell
python app.py
```

### 5. Open in Browser

```
http://localhost:5000
```

## Troubleshooting

### Found 0 unique Chinese characters

If the ingest script reports 0 unique characters, check that your input file contains Chinese text. The input file should be JSON format with a `content` field containing Chinese characters.

### PowerShell syntax

- Use actual values, not `<name>` or `<description>`
- Do not add dashes before commands like `- pip`
- Navigate to the project folder first using `cd`
