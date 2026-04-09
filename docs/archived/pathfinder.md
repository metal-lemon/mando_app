# Pathfinder - Learning Path Builder

**Source:** `templates/archived/pathfinder.html`

## Purpose

Build an ordered learning path through the story library to reach a target text. Users paste target text, and Pathfinder finds stories that efficiently teach the characters needed, minimizing new-character burden at each step.

## Dependencies

- **shared_state.js** - Singleton for known characters, target text/chars
- **data/stories.json** - Story library

## Key Functions

### `extractCharacters(text)`
```javascript
function extractCharacters(text) {
    const chineseRegex = /[\u4e00-\u9fff]/g;
    const matches = text.match(chineseRegex);
    if (!matches) return [];
    return [...new Set(matches)];
}
```

### `findBestStory(knownSet, remainingTargets)`
Greedy algorithm that selects the story maximizing `targets / jumpsize` ratio.
```javascript
function findBestStory(knownSet, remainingTargets) {
    let bestStory = null;
    let bestScore = -Infinity;
    let bestJumpsize = Infinity;

    for (const story of stories) {
        const storyChars = new Set(story.characters || []);
        const newChars = [...storyChars].filter(c => !knownSet.has(c));
        const targets = newChars.filter(c => remainingTargets.has(c));
        const nonTargets = newChars.length - targets.length;
        const jumpsize = newChars.length;

        if (targets.length > 0 && jumpsize <= 50) {
            const score = targets.length / (jumpsize || 1);
            if (score > bestScore || (score === bestScore && jumpsize < bestJumpsize)) {
                bestScore = score;
                bestStory = story;
                bestJumpsize = jumpsize;
            }
        }
    }

    return bestStory ? { story: bestStory, jumpsize: bestJumpsize, targets: ... } : null;
}
```

### `buildPath()`
Main async loop that iteratively selects stories until all target characters are covered.

## Algorithm

1. **Initialize**: Known set from shared_state, remaining targets = target chars - known chars
2. **Loop** while targets remain:
   - Find best story (highest score, within jumpsize ≤ 50)
   - Add all new characters from story to known set
   - Remove covered targets from remaining set
   - Render lesson item
   - Update progress bar
3. **Output**: Ordered list of lessons

## Data Flow

1. Text entered manually or loaded from shared_state (set by "Can I Read This")
2. Characters extracted → split into known vs unknown
3. Build path button triggers greedy algorithm
4. Results displayed as ordered lesson list with stats (jumpsize, remainder)

## UI Patterns

- **Header**: Gradient green (#11998e → #38ef7d), home button
- **Setup status**: File status with success/error/warning states
- **Stats grid**: Card layout for total/known/to-learn counts
- **Progress bar**: Animated gradient fill
- **Lesson list**: Items showing step#, title, jumpsize, remainder

## Error Handling

- If no story can cover remaining targets → show unreachable characters
- Stop button allows early exit with partial path export

## Reuse Ideas

- The greedy scoring algorithm could power any "best next content" selection
- Progress callback pattern useful for long-running operations
- Export format could standardize curriculum sharing between tools
