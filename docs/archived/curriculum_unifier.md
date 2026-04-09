# Curriculum Unifier - Multi-Source Learning Path Builder

**Source:** `templates/archived/curriculum_unifier.html`

## Purpose

Build learning paths using multiple content sources (stories, Wikipedia, classics). More advanced than pathfinder with multiple algorithms, pool generation, clustering, and path optimization.

## Dependencies

- **shared_state.js** - Singleton for known characters
- **user_data/stories_data.json** - Pre-processed story data
- **data/stories.json** - Source story library

## Key Functions

### Character Extraction
```javascript
function extractCharacters(text) {
    const chineseRegex = /[\u4e00-\u9fff]/g;
    const matches = text.match(chineseRegex);
    if (!matches) return [];
    return [...new Set(matches)];
}
```

### Frequency Table Building
```javascript
function buildFrequencyTable() {
    frequencyTable.clear();
    for (const story of stories) {
        const chars = story.characters || [];
        for (const char of chars) {
            frequencyTable.set(char, (frequencyTable.get(char) || 0) + 1);
        }
    }
}
```

### Full Algorithm - Complex Scoring
```javascript
function calculateScore(targets, nonTargets, targetCharsArray, remainingFreq) {
    const jumpsize = targets + nonTargets;
    if (jumpsize === 0) return -Infinity;

    // Component A: Jumpsize Reward
    const scoreA = 10000 / Math.max(jumpsize, 1);

    // Component B: Non-Target Penalty (reduced)
    const scoreB = nonTargets === 0 ? 50000 : -5000 * nonTargets;

    // Component C: Target Count Reward
    const scoreC = (5 - targets) * 1000;

    // Component D: Coverage Ratio
    const scoreD = (targets / jumpsize) * 2000;

    // Component E: Target Count Bonus
    const scoreE = 6000 - (targets * 1000);

    // Component F: NonTarget Penalty
    const scoreF = 2000 - (nonTargets * 2000);

    // Component 4: Enhanced Frequency Bonus
    let score4 = 0;
    if (targetCharsArray && frequencyScoreTableSize > 0) {
        for (const char of targetCharsArray) {
            const entry = frequencyScoreTable.find(e => e.char === char);
            if (entry) {
                score4 += ((frequencyScoreTableSize - entry.id + 1) / frequencyScoreTableSize) * (5000 / jumpsize);
            }
        }
    }

    const rawScore = scoreA + scoreB + scoreC + scoreD + scoreE + scoreF + score4;
    const efficiency = targets / jumpsize;
    return rawScore * efficiency;
}
```

### Greedy Algorithm - Simple Efficiency
```javascript
function findStoryForStepGreedy(knownSet, remainingTargets, minTargets = 1, maxJumpsize = 100) {
    let bestStory = null;
    let bestScore = -Infinity;

    for (const story of stories) {
        const storyChars = new Set(story.characters || []);
        const newChars = [...storyChars].filter(c => !knownSet.has(c));
        const targets = newChars.filter(c => remainingTargets.has(c));
        const nonTargets = newChars.length - targets.length;
        const jumpsize = newChars.length;

        // Simple constraint: targets >= nonTargets (efficient)
        if (targets.length >= minTargets && jumpsize <= maxJumpsize && targets.length >= nonTargets) {
            const score = targets.length / (nonTargets + 1);
            if (score > bestScore) {
                bestScore = score;
                bestStory = story;
            }
        }
    }
    return bestStory ? { story: bestStory, jumpsize: jumpsize, score: bestScore } : null;
}
```

### Pool Generation
```javascript
async function generatePool() {
    // Filter stories by efficiency threshold
    const pool = [];
    for (const story of stories) {
        const storyChars = new Set(story.characters || []);
        const newChars = [...storyChars].filter(c => !knownSet.has(c));
        const targets = newChars.filter(c => remainingTargets.has(c));
        const nonTargets = newChars.length - targets.length;
        
        if (targets.length > 0) {
            const efficiency = targets.length / (nonTargets + 1);
            if (efficiency >= threshold) {
                pool.push({
                    story,
                    targets,
                    nonTargets,
                    jumpsize: newChars.length,
                    efficiency
                });
            }
        }
    }
    // Sort by efficiency descending
    pool.sort((a, b) => b.efficiency - a.efficiency);
}
```

### Path Optimization
```javascript
async function optimizePath(lessons, knownSet, targetChars) {
    let improved = true;
    while (improved && !stopRequested) {
        improved = false;
        // Find biggest jumpsize lesson
        // Try to find alternative story with smaller jumpsize
        // If found, replace in lessons array
    }
}
```

## Algorithms

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| **Full** | Complex multi-component scoring with frequency bonuses | Optimal path when time is not critical |
| **Greedy** | Simple targets/nonTargets ratio | Fast path building |
| **API** | External source search (not implemented) | Future: Wikipedia/classics |

## Modes

| Mode | Description |
|------|-------------|
| **Build Path** | Ordered lesson sequence |
| **Generate Pool** | All candidates above threshold |
| **Find Clusters** | Group similar content |

## Data Flow

1. User pastes target text → characters extracted
2. Select algorithm and mode
3. Build button triggers:
   - Load stories from user_data/
   - Build frequency table
   - Run selected algorithm
   - Display progress/lessons/pool
4. Optional: optimize path, find clusters, export

## UI Patterns

- **Setup modal**: Instructions for user_data folder
- **Source selector**: Dropdown for content sources
- **Algorithm/mode buttons**: Toggle selection
- **Progress bar**: Animated fill with stats
- **Pool list**: Scrollable with efficiency scores

## Reuse Ideas

- Frequency table concept could power character difficulty rankings
- Pool generation is reusable for any "find all candidates" feature
- Optimization algorithm could apply to any ordered content
- The multi-algorithm router pattern is extensible for new sources
