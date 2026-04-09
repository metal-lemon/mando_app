Last updated: 2026-04-09

# Can I Read This? - Text Readability Analyzer

**Source:** `templates/archived/can_i_read_this.html`

## Table of Contents

1. [Purpose](#1-purpose)
2. [Dependencies](#2-dependencies)
3. [Key Functions](#3-key-functions)
4. [Two Metrics](#4-two-metrics)
5. [Data Flow](#5-data-flow)
6. [Features](#6-features)
7. [UI Patterns](#7-ui-patterns)
8. [Thresholds](#8-thresholds)
9. [Reuse Ideas](#9-reuse-ideas)

---

## 1. Purpose

Analyze any Chinese text to determine what percentage of characters the user knows. Provides detailed readability statistics, shows which characters need to be learned, and allows adding characters directly to the known set.

Also supports traditional→simplified character conversion.

---

## 2. Dependencies

- **shared_state.js** - Singleton for known characters
- **data/trad_simp_map.json** - Traditional→simplified mapping

---

## 3. Key Functions

### Readability Analysis

```javascript
function analyzeTextWithSet(text, state) {
    const chineseRegex = /[\u4e00-\u9fff]/g;
    const allChars = text.match(chineseRegex);
    if (!allChars || allChars.length === 0) return false;

    const totalChars = allChars.length;
    const uniqueChars = new Set(allChars);
    const uniqueTotal = uniqueChars.size;

    // Count occurrences (by position) vs unique
    const knownCount = allChars.filter(ch => state.has(ch)).length;
    const unknownUnique = Array.from(uniqueChars).filter(ch => !state.has(ch));
    const knownUniqueCount = uniqueTotal - unknownUnique.length;

    const uniquePercent = (knownUniqueCount / uniqueTotal) * 100;
    const occurrencePercent = (knownCount / totalChars) * 100;

    return { uniquePercent, occurrencePercent, unknownUnique };
}
```

### Traditional Character Detection

```javascript
// Separate traditional from non-traditional unknowns
const tradUnknown = unknownUnique.filter(ch => tradMap.has(ch));
const nonTradUnknown = unknownUnique.filter(ch => !tradMap.has(ch));
```

### Traditional → Simplified Conversion

```javascript
function convertToSimplified() {
    let converted = text;
    let count = 0;
    for (let [trad, simp] of tradMap) {
        if (text.includes(trad)) {
            const regex = new RegExp(trad, 'g');
            converted = converted.replace(regex, simp);
            count++;
        }
    }
    return converted;
}
```

### Readability Advice

```javascript
function getReadabilityAdvice(percentage) {
    if (percentage >= 98) return {
        text: "🎉 Excellent! You can read this text comfortably...",
        class: "advice-excellent"
    };
    if (percentage >= 95) return {
        text: "👍 Good! You'll understand the main ideas well...",
        class: "advice-good"
    };
    if (percentage >= 90) return {
        text: "📚 Challenging but doable...",
        class: "advice-challenging"
    };
    return {
        text: "⚠️ Difficult - consider a different text...",
        class: "advice-difficult"
    };
}
```

---

## 4. Two Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **% Known (Occurrence)** | known chars / total chars | Measures reading flow, how often you stop |
| **% Known (Unique)** | known unique / total unique | Measures vocabulary coverage |

**Note:** Occurrence% is typically higher because common characters repeat more.

---

## 5. Data Flow

1. User loads/merges character file OR loads example
2. User pastes text to analyze
3. Analyze button triggers:
   - Extract characters via regex
   - Calculate both percentage metrics
   - Separate traditional vs simplified unknowns
   - Generate advice based on unique%
   - Render results with clickable unknown characters

---

## 6. Features

1. **Load & merge**: Upload JSON to add to known set
2. **Analyze text**: Real-time readability calculation
3. **Traditional conversion**: Convert trad→simp before analyzing
4. **Click to learn**: Click any unknown character to add to known set
5. **Save to stories**: Send text to story library
6. **Export unknown**: Download unknown chars as JSON

---

## 7. UI Patterns

- **Stats grid**: Three stat cards (occurrence%, unique%, learning gap)
- **Progress bar**: Visual fill showing known percentage
- **Learning gap section**: Clickable character tiles, color-coded (red=simp, purple=trad)
- **Advice box**: Color-coded guidance based on difficulty
- **Traditional indicator**: Shows count of trad chars found

---

## 8. Thresholds

| Range | Class | Advice |
|-------|-------|--------|
| ≥98% | excellent | Comfortable reading |
| 95-97% | good | Minor lookups needed |
| 90-94% | challenging | Preview chars first |
| <90% | difficult | Consider easier text |

---

## 9. Reuse Ideas

- The two-metric analysis (occurrence vs unique) provides nuanced readability
- Traditional→simplified map could power any conversion feature
- Clickable tiles pattern for adding to known set is reusable
- The advice thresholds could be configurable
- Export format for unknown chars could standardize with other tools