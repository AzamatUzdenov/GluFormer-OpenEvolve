# OpenEvolve × GluFormer Execution Report

**Task:** Improve HbA1c prediction from GluFormer embeddings using OpenEvolve.
**LLM:** claude-sonnet-4-6 | **Iterations:** 20 | **Seed:** 42

---

## What Was Changed

**Target:**
- **[1] Feature selection:** baseline uses only the 1024-dim GluFormer embeddings (`Representation`). Evolved version was free to use `GMI` only, `Representation` only, or both concatenated.
- **[2] Model & Hyperparameters:** baseline uses `Ridge(alpha=80)` with no feature scaling.

OpenEvolve evolved the block autonomously using `claude-sonnet-4-6` over 20 iterations.

---

## Results

| Metric | Baseline | Evolved | Delta |
|--------|----------|---------|-------|
| **Combined score** | 0.5956 | **0.6207** | +0.0250 |
| **Pearson r** | 0.4507 | **0.4631** | +0.0124 |
| **Spearman r** | 0.5002 | **0.5404** | +0.0402 |
| **Prediction stability** | 0.9745 | **0.9773** | +0.0029 |

All four metrics improved. **Winner: EVOLVED.**

---

## Did It Help?

Yes. The most meaningful gain is **Spearman r (+0.04)**. The evolved model ranks patients more correctly by HbA1c risk, which matters clinically. Pearson r improved by +0.012 and prediction stability slightly increased, meaning the evolved predictor is both more accurate and more consistent across random CV splits.
