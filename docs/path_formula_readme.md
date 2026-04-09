Last updated: 2026-04-09

# Path Formula Configuration

This file stores different scoring formula configurations for the Curriculum Builder's path optimization algorithm.

## Table of Contents

1. [Formula Sets](#1-formula-sets)
2. [How to Swap Formulas](#2-how-to-swap-formulas)
3. [Test Results Summary](#3-test-results-summary)
4. [Detailed Path Comparison](#4-detailed-path-comparison)
5. [Conclusion](#5-conclusion)
6. [Files](#6-files)

---

## 1. Formula Sets

| Set | Name | Description |
|-----|------|-------------|
| 1 | Original - Efficient Paths | Original scoring - aims for fewer lessons |
| 2 | Frequency Scoring | Added frequency bonus - moderate slowness |
| 3 | Small Jumps + Zero Non-Targets | Aggressive slowness - aims for jumpsize < 5 |

---

## 2. How to Swap Formulas

Edit `curriculum_builder.html` and replace the `calculateScore()` function with the desired formula set from `path_formula_bin.py`.

---

## 3. Test Results Summary

**Target Text:** 小老鼠打电话 (71 unknown characters)

| Version | Date | Formula Set | Lessons | Total Jumpsize | Avg Jumpsize |
|---------|------|-------------|---------|----------------|--------------|
| v1 | 01-09 AM | Initial | 11 | ~220 | ~20 |
| Original | 01-42 AM | Set 1 | 24 | ~420 | ~17.5 |
| +Freq | 02:58 AM | Set 2 | 22 | ~380 | ~17.3 |
| 5-comp | 03:26 AM | Set 2 extended | 24 | ~400 | ~16.7 |
| A-F | 03:38 AM | Set 3 | 24 | ~400 | ~16.7 |

---

## 4. Detailed Path Comparison (Latest Versions)

| Step | Story | jumpsize | targets | nonTargets | remainder |
|------|-------|----------|---------|------------|------------|
| 1 | 小白兔蹦蹦跳 | 14 | 2 | 12 | 69 |
| 2 | 幼儿园的花园 | 21 | 3 | 18 | 66 |
| 3 | 数学课上，苏 | 21 | 3 | 18 | 63 |
| 4 | 一天，小猪来 | 21 | 3 | 18 | 60 |
| 5 | 熊宝宝、熊妈 | 21 | 7 | 14 | 53 |
| 6 | "咕嚕咕嚕… | 20 | 4 | 16 | 49 |
| 7 | 小熊猫第一天 | 18 | 2 | 16 | 47 |
| 8 | 城里来了个大 | 18 | 3 | 15 | 44 |
| 9 | 小狗巴儿捧着 | 18 | 4 | 14 | 40 |
| 10 | 一只黑色小鼹 | 18 | 4 | 14 | 36 |
| 11 | 下雪啦！白白 | 17 | 1 | 16 | 35 |
| 12 | 山羊爷爷在地 | 17 | 1 | 16 | 34 |
| 13 | 猫儿交了一个 | 17 | 1 | 16 | 33 |
| 14 | 小熊和小喜鹊 | 17 | 1 | 16 | 32 |
| 15 | 小蛇又吃多了 | 17 | 1 | 16 | 31 |
| 16 | 大乌龟爬山坡 | 17 | 2 | 15 | 29 |
| 17 | 阳光明媚的一 | 18 | 2 | 16 | 27 |
| 18 | 他比姐姐小一 | 18 | 2 | 16 | 25 |
| 19 | 小猫钓鱼回来 | 18 | 1 | 17 | 24 |
| 20 | 小松鼠放学回 | 18 | 2 | 16 | 22 |
| 21 | 水根爷爷在菜 | 18 | 2 | 16 | 20 |
| 22 | 在一个大森林 | 18 | 2 | 16 | 18 |
| 23 | 冬天到了，天 | 18 | 18 | 0 | 0 |
| 24 | 小老鼠打电话 | 0 | 0 | 0 | 0 |

---

## 5. Conclusion

### All formula variations produce nearly identical results (22-24 lessons).

The algorithm appears to be constrained by the **story library** more than the scoring formula:

1. **No stories exist** with jumpsize < 5 that cover the target characters
2. **Non-target characters** are unavoidable because stories contain fixed character sets
3. **Target coverage** requires accepting some non-target characters (average ~15 per lesson)

### Key Observations

- **Steps 1-10**: Consistently cover 2-7 targets with 12-18 non-targets (jumpsize 14-21)
- **Steps 11-22**: Finally reach 1-2 targets per lesson, but still 15-17 non-targets
- **Step 23**: Final story "冬天到了，天" covers remaining 18 targets at once

### What This Means

The story library is the limiting factor, not the algorithm. To achieve truly slow paths with:
- jumpsize < 5
- targets < 5
- nonTargets = 0

Would require either:
1. A much larger/better story library with more granular stories
2. A different algorithm that can "split" stories into smaller chunks
3. Accepting that the current library forces ~15-20 char jumpsizes

---

## 6. Files

- `path_formula_bin.py` - Python file containing formula definitions
- `docs/path_formula_readme.md` - This file