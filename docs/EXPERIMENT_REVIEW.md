# Experiment review, 3 October 2026

## Contribution and source separation

Azamat Uzdenov authored the initial integration commit on 11 June 2026 and is credited for `gluformer_openevolve/` in NOTICE. This includes a baseline, evolution configuration, evaluator, launcher, comparison script, selected candidate and saved aggregate metrics. GluFormer itself is upstream work, retained under its Apache-2.0 license; the encoder was not retrained in this experiment.

## What the saved experiment establishes

The pipeline implements LLM-guided code search for an HbA1c regression head over frozen GluFormer embeddings. The selected candidate blends GMI-only RidgeCV (70%) with a scaled embedding Ridge model (30%). Stored search-CV values show a modest increase over an unscaled embedding-only baseline. They demonstrate a prototype workflow and a candidate for follow-up, not validated model superiority or clinical benefit.

## Remaining evaluation issues

- Search repeatedly reuses 5 folds across 10 seeds; these scores are development/selection evidence.
- GMI is added to the selected candidate but absent from the baseline. Use the same inputs and a strong matched baseline to isolate the search's contribution.
- Targets are z-scored separately inside each training fold, but predictions are not inverse-transformed before pooling folds. Correct this before treating pooled correlations as reliable evidence.
- Participant-ID normalization, joins and exclusions need an explicit audit. Their code is present, but no new participant-level data review or experimental rerun was performed here.
- `1 - std(Pearson across seeds)` measures consistency of correlation estimates, not clinical prediction stability. No held-out cohort, clinical-unit HbA1c error or uncertainty interval is established.
- Data resolution in the historical scripts depends on the working directory. Run from `gluformer_openevolve/` as documented.

## Data and publication provenance

The three Shanghai demo CSV files and tokenized training example are byte-identical to files already available in the public upstream GluFormer repository at the time of this review. The review compared Git blob hashes without displaying individual records. No private Segal-lab 10K/HPP participant data, new model checkpoints or credentials were added. Follow upstream/original dataset terms for reuse; public availability is not a new grant of data rights.

A scan of all advertised branch/history text objects found credential placeholders, not live credentials. The repository has one original commit, one branch, no tags, releases or issues at this review point. This is a focused release review, not a formal security audit. Training/search and original data values were not rerun/reviewed during this preparation.

Documentation was clarified with Codex assistance for publication preparation; historical experiment code and saved metrics were preserved.
