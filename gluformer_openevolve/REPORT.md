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

All four saved search-CV metrics increased. The candidate was selected using these same development scores; this is not a held-out test result.

---

## Interpretation and limitations

This run demonstrates an implemented OpenEvolve-guided search for a small prediction head on frozen GluFormer representations. The saved Spearman and Pearson scores increased, but they do not establish clinical accuracy, risk stratification or a validated improvement of GluFormer itself.

The search reused the same CV folds; the selected candidate also adds GMI, so the inputs are not matched to the baseline. The historical target scaling is not inverted before predictions from different folds are pooled. Fix this harness and evaluate matched baselines on a test set untouched by model selection before drawing performance conclusions.

The historical run/model provenance is recorded above, as originally saved; the model was not rerun or its runtime independently recovered during this 3 October 2026 review. A saved best-program metadata file is retained. "Prediction stability" means 1 minus the standard deviation of Pearson correlations across seeds, not patient-level or clinical stability.

Author of the OpenEvolve integration/experiment: Azamat Uzdenov. Upstream GluFormer authors and license are retained in the root README and NOTICE.
