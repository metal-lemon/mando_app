Last updated: 2026-04-09

# Sort Function Toolbox

This toolbox contains all the techniques developed and discussed for generating pedagogically efficient lesson sequences from a record corpus. Each tool can be used independently or chained together. The tools are organised by their role in the pipeline.

## Table of Contents

1. [Tool Index](#1-tool-index)
2. [Detailed Tool Descriptions](#2-detailed-tool-descriptions)
3. [Recommended Workflows](#3-recommended-workflows)
4. [Summary Table of Tool Complexities](#4-summary-table-of-tool-complexities)

---

## 1. Tool Index

| # | Tool Name | Category |
|---|-----------|----------|
| 1 | Numerical Cut-off | Pre-filtering |
| 2 | Pre-split by Known Set | Precomputation |
| 3 | Efficiency-Threshold Pool Building | Pool Selection |
| 4 | Overlap-Based Greedy Ordering | Sequencing (fast) |
| 5 | Target Anchor (Capstone Lesson) | Final Step |
| 6 | Jaccard Clustering (Character Reuse Grouping) | Clustering |
| 7 | Budget-Aware Story Packing | Sub-pool Selection |
| 8 | Candidate Sub-pool Generator | Alternative Generation |
| 9 | Exact Sub-pool Optimiser | Small Pool Optimisation |
| 10 | Lookahead Beam Search (Proposal #7) | Sequencing (optimal) |
| 11 | Character Frequency Bonus | Heuristic for Beam Search |

---

## 2. Detailed Tool Descriptions

### 1. Numerical Cut-off (Size-based Pruning)

- **Purpose**: Quickly discard records that are too long to ever be efficient.
- **Formula**: Keep record if `unique_count <= |K| + alpha * |T|` (e.g., alpha = 2).
- **Complexity**: O(1) per record.
- **When to use**: First step when processing a large corpus (millions of records).

### 2. Pre-split by Known Set (Split-on-Known)

- **Purpose**: For each record, precompute target and non-target characters relative to the initial known set.
- **Output**: `target_unknown`, `non_target_unknown`, `target_count`, `non_target_count`.
- **When to use**: After numerical cut-off, before any pool building or ordering.

### 3. Efficiency-Threshold Pool Building (Cover-First)

- **Purpose**: Select a pool of records that together cover all target characters, using a relaxed efficiency threshold (e.g., `targets / (nonTargets+1) >= theta`).
- **Output**: A pool (list of records) that guarantees coverage.
- **When to use**: After pre-split, to create a candidate set for further optimisation.

### 4. Overlap-Based Greedy Ordering (Greedy Known-Overlap)

- **Purpose**: Order a set of records by repeatedly picking the record that shares the most characters with the learner's current knowledge.
- **Cost function**: Maximise `|record-text.chars intersect currentKnown|`.
- **Complexity**: O(N^2) for a pool of size N.
- **When to use**: Fast sequencing when the pool is already efficient and you don't need optimal ordering.

### 5. Target Anchor (Capstone Lesson)

- **Purpose**: Place the original target text as the final lesson after all its characters are known.
- **Benefit**: No new characters introduced; serves as a rewarding reading exercise.
- **When to use**: Always append after the sequenced records.

### 6. Jaccard Clustering (Character Reuse Grouping)

- **Purpose**: Identify clusters of records that share many non-target characters (high Jaccard similarity), then select the cluster with the smallest union of non-targets.
- **Steps**:
  1. Compute pairwise Jaccard on `non_target_unknown` sets.
  2. Build graph with edges where Jaccard >= threshold.
  3. Extract dense subgraphs (cliques).
  4. Choose cluster with minimal union size.
- **When to use**: After pool building, to focus on a subset that maximises character reuse.

### 7. Budget-Aware Story Packing (Greedy Packing)

- **Purpose**: Select a subset of records that maximises the number of records while keeping the total distinct non-target characters <= budget `K`.
- **Algorithm**: Greedy - always add the record that introduces the fewest *new* non-targets given the current union.
- **Output**: A sub-pool (list of records) respecting the budget.
- **When to use**: When you have a hard limit on how many new non-target characters the learner can handle.

### 8. Candidate Sub-pool Generator (Randomised Packing)

- **Purpose**: Generate multiple candidate sub-pools by running budget-aware greedy with different random record orders.
- **Output**: A list of sub-pools (each a list of record IDs) that all respect the budget and are near-maximal in size.
- **When to use**: To give the instructor options to choose from based on other criteria (topic diversity, length, etc.).

### 9. Exact Sub-pool Optimiser (Brute-Force Packing)

- **Purpose**: For very small pools (N <= 20), exhaustively search all subsets to find the optimal sub-pool that maximises record count under the non-target budget.
- **Complexity**: O(2^N), only feasible for N <= 20.
- **When to use**: When optimality is critical and the pool is tiny.

### 10. Lookahead Beam Search (Proposal #7)

- **Purpose**: Find an ordered sequence of records that minimises the total distinct non-target characters across the whole sequence, using limited lookahead to avoid greedy mistakes.
- **Cost function**: Minimise `|acc_non|` (size of union of non-targets so far).
- **Optional enhancement**: Add character frequency bonus to prioritise common characters early.
- **Parameters**: Beam width `W` (e.g., 10-20), frequency weight `lambda`.
- **Complexity**: `O(W * N * L * C)`. Practical for pools up to 100-200 records (2-3 seconds in Python; <=100 records in JavaScript).
- **When to use**: When the pool is moderately sized (40-200 records) and you want near-optimal sequencing.

### 11. Character Frequency Bonus

- **Purpose**: Encourage covering common characters early by reducing the effective cost when a record covers high-frequency characters.
- **Implementation**: Add `-lambda * Sigma log(freq[c]+1)` to the cost for each new target character `c`.
- **When to use**: As a heuristic inside beam search (Proposal #7) or as a tie-breaker in greedy ordering.

---

## 3. Recommended Workflows

### 1. Full Pipeline

Uses lookahead beam search for optimal sequencing when the pool is moderately sized.

1. **Numerical Cut-off** - Reduce corpus to manageable size.
2. **Pre-split by Known Set** - Precompute target/non-target sets for each record.
3. **Efficiency-Threshold Pool Building** - Create a pool that covers all targets.
4. **Jaccard Clustering** (optional) - Find a dense, reuse-friendly sub-pool.
5. **Budget-Aware Story Packing** (optional) - Enforce a hard limit on distinct non-targets.
6. **Candidate Sub-pool Generator** (optional) - Produce alternatives for instructor review.
7. **Lookahead Beam Search** (Proposal #7) - Optimise the sequence order.
8. **Target Anchor** - Append the original text as the final lesson.

### 2. Fast Pipeline

Uses greedy ordering instead of beam search for fast, less optimal results.

1. **Numerical Cut-off** - Reduce corpus to manageable size.
2. **Pre-split by Known Set** - Precompute target/non-target sets for each record.
3. **Efficiency-Threshold Pool Building** - Create a pool that covers all targets.
4. **Jaccard Clustering** (optional) - Find a dense, reuse-friendly sub-pool.
5. **Budget-Aware Story Packing** (optional) - Enforce a hard limit on distinct non-targets.
6. **Candidate Sub-pool Generator** (optional) - Produce alternatives for instructor review.
7. **Overlap-Based Greedy Ordering** - Fast sequencing instead of beam search.
8. **Target Anchor** - Append the original text as the final lesson.

---

## 4. Summary Table of Tool Complexities

| Tool | Time Complexity | Space Complexity | Typical Input Size |
|------|-----------------|------------------|---------------------|
| Numerical Cut-off | O(#records) | O(1) | millions |
| Pre-split by Known Set | O(#records * avg_unique) | O(#records * avg_unique) | thousands |
| Efficiency-Threshold Pool | O(pool_candidates^2) | O(pool_candidates^2) | thousands -> hundreds |
| Overlap Greedy Ordering | O(pool^2) | O(pool) | <= 500 |
| Jaccard Clustering | O(pool^2 * avg_unique) | O(pool^2) | <= 200 |
| Budget-Aware Packing | O(pool^2) | O(pool) | <= 200 |
| Exact Sub-pool Optimiser | O(2^N) | O(2^N) | N <= 20 |
| Lookahead Beam Search | O(W * N * L * C) | O(W * N) | N <= 200 |
| Target Anchor | O(1) | O(1) | always |

---

This toolbox provides a complete, modular, and scalable set of techniques for generating efficient Chinese character curricula from any record corpus. You can mix and match tools depending on your performance requirements and pedagogical goals.
