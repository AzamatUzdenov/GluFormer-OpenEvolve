"""
compare.py: baseline vs evolved comparison across all three metrics.
"""

import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#print(f"SCRIPT_DIR: {SCRIPT_DIR}")

def resolve(p):
    if os.path.isabs(p) and os.path.exists(p): return p
    if os.path.exists(p): return os.path.abspath(p)
    alt = os.path.join(SCRIPT_DIR, p)
    return alt if os.path.exists(alt) else p

from evaluator import evaluate

b_path = resolve(sys.argv[1] if len(sys.argv) > 1 else "initial_program.py")
e_path = resolve(sys.argv[2] if len(sys.argv) > 2 else
                 "openevolve_output/best/best_program.py")

print(f"\n  Baseline : {os.path.basename(b_path)}")
print(f"  Evolved  : {os.path.basename(e_path)}")
print("\n" + "="*66)
print("  GluFormer — HbA1c Prediction Comparison")
print("="*66)

print("  Running baseline (10 seeds × 5 folds)...")
b = evaluate(b_path)
print("  Running evolved  (10 seeds × 5 folds)...")
e = evaluate(e_path)

for res, label in [(b, "Baseline"), (e, "Evolved")]:
    if "error" in res:
        print(f"\n  ERROR [{label}]: {res['error']}")
        sys.exit(1)

rows = [
    ("combined_score",       "Combined score",        True),
    ("pearson_r",            "Pearson r",             True),
    ("spearman_r",           "Spearman r",            True),
    ("prediction_stability", "Prediction stability",  True),
]

print(f"\n  {'Metric':<28} {'Baseline':>10} {'Evolved':>10} {'Delta':>10}")
print(f"  {'-'*28} {'-'*10} {'-'*10} {'-'*10}")
for key, label, higher_better in rows:
    bv = b.get(key, float('nan'))
    ev = e.get(key, float('nan'))
    d  = ev - bv
    mark = "[Better] " if (higher_better and d > 0) else "[Worse] "
    print(f"  {label:<28} {bv:>10.4f} {ev:>10.4f} {d:>+10.4f}  {mark}")

winner = "EVOLVED" if e["combined_score"] > b["combined_score"] else "BASELINE"
print(f"\n  Winner: {winner}  "
      f"(combined_score {e['combined_score']:.4f} vs {b['combined_score']:.4f})")
print("="*66 + "\n")