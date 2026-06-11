# OpenEvolve Setup for GluFormer Model

## Requirements
- `gluformer` conda env (from GluFormer repo)
- `pip install openevolve`
- Anthropic API key

## Files needed (in `GluFormer/demo/`)
- `GluFormer_Representations_Shanghai_2023.csv`
- `Shanghai_GMI.csv`
- `Shanghai_results.csv`

## Directory structure
```
GluFormer/
├── demo/                    # data files
└── gluformer_openevolve/    # all scripts
    ├── initial_program.py
    ├── evaluator.py
    ├── config.yaml
    ├── run_evolution.sh
    └── compare.py
```

## Run

```bash
# Clone this repository
git clone https://github.com/AzamatUzdenov/GluFormer-OpenEvolve.git
cd GluFormer-OpenEvolve

# Create and activate conda environment
conda create -n gluformer python=3.10
conda activate gluformer

# Install dependencies
pip install -r requirements.txt
pip install openevolve

# Verify baseline
python evaluator.py initial_program.py

# Run evolution
export OPENAI_API_KEY="sk-ant-YOUR-ANTHROPIC-KEY"   # use your own Anthropic key — never commit it
bash run_evolution.sh

# Compare between initial and evolved program
python compare.py
```

## Expected output
```
  Combined score     0.5956 → 0.6207  +0.0250
  Pearson r          0.4507 → 0.4631  +0.0124
  Spearman r         0.5002 → 0.5404  +0.0402
  Prediction stability  0.9745 → 0.9773  +0.0029
  Winner: EVOLVED
```