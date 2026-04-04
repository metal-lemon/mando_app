function calculateScore(targets, nonTargets, targetCharsArray, remainingFreq) {
    const jumpsize = targets + nonTargets;
    if (jumpsize === 0) return -Infinity;
    
    // Component A: Jumpsize Reward
    const scoreA = 10000 / Math.max(jumpsize, 1);
    
    // Component B: Non‑Target Penalty (reduced)
    const scoreB = nonTargets === 0 ? 50000 : -5000 * nonTargets;
    
    // Component C: Target Count Reward (less steep)
    const scoreC = (5 - targets) * 1000;
    
    // Component D: Coverage Ratio (unchanged)
    const scoreD = (targets / jumpsize) * 2000;
    
    // Component E: Target Count Bonus (unchanged)
    const scoreE = 6000 - (targets * 1000);
    
    // Component F: NonTarget Penalty (unchanged)
    const scoreF = 2000 - (nonTargets * 2000);
    
    // Component 4: Enhanced Frequency Bonus
    let score4 = 0;
    if (targetCharsArray && frequencyScoreTableSize > 0) {
        for (const char of targetCharsArray) {
            const entry = frequencyScoreTable.find(e => e.char === char);
            if (entry) {
                // More weight to common characters
                score4 += ((frequencyScoreTableSize - entry.id + 1) / frequencyScoreTableSize) * (5000 / jumpsize);
            }
        }
    }
    
    // Component G: Dynamic Remaining Target Frequency Bonus
    let scoreG = 0;
    if (remainingFreq && targetCharsArray) {
        for (const char of targetCharsArray) {
            scoreG += (remainingFreq[char] || 0) * 1000;
        }
    }
    
    return scoreA + scoreB + scoreC + scoreD + scoreE + scoreF + score4 + scoreG;
}