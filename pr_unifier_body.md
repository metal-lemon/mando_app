## Summary

Adds a new unified tool `curriculum_unifier.html` that combines all curriculum builder features into a single interface.

### Features

- **Source Selector**: Choose between Story Library + 4 placeholder sources (Wikipedia, Classics, News, Custom) for future expansion
- **Algorithm Selection**: 
  - Full (Complex) - uses multi-component scoring with maxJumpsize constraints
  - Greedy (Efficient) - simple targets/nonTargets ratio
  - API Search (coming soon) - stub for external sources
- **Mode Selection**:
  - Build Path - full curriculum with optimization
  - Generate Pool - candidate pool generation
  - Find Clusters - Jaccard-style clustering analysis

### Preserved Methods

All optional methods from original builders are preserved:
- `calculateScore()` - complex multi-component scoring (from curriculum_builder)
- `findStoryForStepFull()` - full algorithm with maxJumpsize
- `findStoryForStepOld()` - legacy reference
- `findStoryForStepGreedy()` - efficient greedy selection (from lite_builder)
- `findStoryForStepAPI()` - stub for external sources
- `findCluster()` - Jaccard clustering
- `optimizePath()` - post-processing optimization

### Testing

```
python app.py
# Open http://localhost:5000/curriculum_unifier
```