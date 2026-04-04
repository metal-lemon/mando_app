"""
Path Formula Configurations for Curriculum Builder
Stored formulas for different optimization strategies
"""

# =============================================================================
# FORMULA SET 1: Original (efficient paths)
# =============================================================================
FORMULA_SET_1 = {
    "name": "Original - Efficient Paths",
    "description": "Original scoring components - aims for fewer lessons",
    "components": [
        {
            "id": 1,
            "name": "CoverageRatio",
            "formula": "(targets / jumpsize) * 2000",
            "description": "Rewards covering MORE targets relative to jumpsize"
        },
        {
            "id": 2,
            "name": "JumpsizeQuality",
            "formula": "2000 - (targets - 1) * 200 - nonTargets * 400",
            "description": "Base 2000, -200 per extra target, -400 per non-target"
        }
    ],
    "return": "score1 + score2"
}


# =============================================================================
# FORMULA SET 2: Frequency Scoring (moderate slowness)
# =============================================================================
FORMULA_SET_2 = {
    "name": "Frequency Scoring - Moderate Slowness",
    "description": "Added frequency bonus and target count bonus - aims for ~1 target per lesson",
    "components": [
        {
            "id": 1,
            "name": "CoverageRatio",
            "formula": "(targets / jumpsize) * 2000",
            "description": "Rewards covering MORE targets relative to jumpsize"
        },
        {
            "id": 2,
            "name": "JumpsizeQuality",
            "formula": "2000 - (targets - 1) * 200 - nonTargets * 400",
            "description": "Base 2000, -200 per extra target, -400 per non-target"
        },
        {
            "id": 3,
            "name": "TargetCountBonus",
            "formula": "6000 - (targets * 1000)",
            "description": "Rewards FEWER targets (1 target = 5000, 2 = 4000...)"
        },
        {
            "id": 4,
            "name": "FrequencyBonus",
            "formula": "sum((char_id / frequencyScoreTableSize) * (2000 / jumpsize))",
            "description": "Rewards covering common characters"
        },
        {
            "id": 5,
            "name": "NonTargetPenalty",
            "formula": "2000 - (nonTargets * 2000)",
            "description": "Penalizes non-targets (0 = 2000, 1 = 0, 2 = -2000...)"
        }
    ],
    "return": "score1 + score2 + score3 + score4 + score5"
}


# =============================================================================
# FORMULA SET 3: Small Jumps + Zero Non-Targets (slowest paths)
# =============================================================================
FORMULA_SET_3 = {
    "name": "Small Jumps + Zero Non-Targets",
    "description": "Aims for jumpsize < 5, targets < 5, nonTargets = 0",
    "components": [
        {
            "id": "A",
            "name": "JumpsizeReward",
            "formula": "10000 / max(jumpsize, 1)",
            "description": "Smaller jumpsize = better (10000/1=10000, 10000/5=2000)"
        },
        {
            "id": "B",
            "name": "NonTargetPenalty",
            "formula": "50000 if nonTargets == 0 else -10000 * nonTargets",
            "description": "Zero nonTargets = +50000, otherwise severe penalty"
        },
        {
            "id": "C",
            "name": "TargetCountReward",
            "formula": "(5 - targets) * 2500",
            "description": "Fewer targets = better (1 target = 10000, 5 targets = 0)"
        },
        {
            "id": "D",
            "name": "CoverageRatio",
            "formula": "(targets / jumpsize) * 2000",
            "description": "Kept from original"
        },
        {
            "id": "E",
            "name": "TargetCountBonus",
            "formula": "6000 - (targets * 1000)",
            "description": "Kept from set 2"
        },
        {
            "id": "F",
            "name": "NonTargetPenalty",
            "formula": "2000 - (nonTargets * 2000)",
            "description": "Kept from set 2"
        },
        {
            "id": 4,
            "name": "FrequencyBonus",
            "formula": "sum((char_id / frequencyScoreTableSize) * (2000 / jumpsize))",
            "description": "Rewards covering common characters"
        }
    ],
    "return": "scoreA + scoreB + scoreC + scoreD + scoreE + scoreF + score4"
}


# =============================================================================
# Active formula set selection
# =============================================================================
# Change this to select which formula set to use:
# - FORMULA_SET_1: Original efficient paths
# - FORMULA_SET_2: Frequency scoring (moderate slowness)
# - FORMULA_SET_3: Small jumps + zero non-targets (slowest)
ACTIVE_FORMULA = FORMULA_SET_3


if __name__ == "__main__":
    print(f"Active Formula: {ACTIVE_FORMULA['name']}")
    print(f"Description: {ACTIVE_FORMULA['description']}")
    print(f"Components: {len(ACTIVE_FORMULA['components'])}")
    print(f"Return: {ACTIVE_FORMULA['return']}")
