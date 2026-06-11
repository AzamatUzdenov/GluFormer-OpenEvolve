# GluFormer + OpenEvolve

GluFormer is a foundation model for continuous glucose monitoring (CGM). It turns a person's glucose history into a 1024-number "fingerprint" (an embedding).

This repo takes those embeddings and uses [OpenEvolve](https://github.com/codelion/openevolve) (an open-source take on DeepMind's AlphaEvolve) to automatically find a better little model that predicts HbA1c, the blood marker for average glucose over ~3 months. GluFormer itself stays frozen; only the small model on top gets evolved.

## How it works

OpenEvolve keeps asking an LLM to rewrite one block of code, scores each version with cross-validation, and keeps the best ones. Basically natural selection for code. The only thing that changes is the prediction "head"; data loading and scoring stay fixed.

Everything lives in `gluformer_openevolve/`:

| File | What it does |
|------|------|
| `initial_program.py` | starting code, with the evolvable part marked off |
| `evaluator.py` | scores each version (cross-validated) |
| `config.yaml` | evolution settings and the task prompt for the LLM |
| `openevolve_output/best/` | the best version it found |

## Did it help?

A bit, yes:

| Metric | Before | After |
|--------|--------|-------|
| Combined score | 0.5956 | 0.6207 |
| Pearson r | 0.4507 | 0.4631 |
| Spearman r | 0.5002 | 0.5404 |
| Stability | 0.9745 | 0.9773 |

The evolved version scales the features and mixes in GMI (a simple glucose proxy the baseline ignored). The biggest win is ranking patients by risk more correctly (Spearman).

## Run it

```bash
cd gluformer_openevolve
python evaluator.py initial_program.py   # baseline
bash run_evolution.sh                     # evolve (needs your own Anthropic API key)
python compare.py                         # baseline vs evolved
```

More detail in `gluformer_openevolve/README.md` and `gluformer_openevolve/REPORT.md`.

## Credit

Built on GluFormer by Guy Lutsker, Gal Sapir, Smadar Shilo, Hagai Rossman, Eran Segal and colleagues. Their code is included here under Apache-2.0; I just added the OpenEvolve part on top.

- Original repo: https://github.com/Guylu/GluFormer
- Original README: [docs/GLUFORMER_UPSTREAM.md](docs/GLUFORMER_UPSTREAM.md)
- Paper: *A foundation model for continuous glucose monitoring data*, Nature (2026), https://doi.org/10.1038/s41586-025-09925-9

License: Apache-2.0 (see [LICENSE](LICENSE) and [NOTICE](NOTICE)).
