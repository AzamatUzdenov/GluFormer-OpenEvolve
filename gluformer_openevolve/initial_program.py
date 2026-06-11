"""
GluFormer: HbA1c prediction from GluFormer embeddings + GMI
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from scipy.stats import spearmanr


# --- helpers ----------------------------------------------------------------------------------------------------

ROOT_DIR = os.path.dirname(os.getcwd())
#print(f"ROOT_DIR: {ROOT_DIR}")

def normalize_participant_id(x):
    """Strip leading prefix digit: 1001020210730 → 100102, 1.00102E+12 → 100102"""
    return int(str(int(float(x)))[1:7])


def _find(filename, script_dir=ROOT_DIR):
    candidates = [
        script_dir,
        os.path.join(script_dir, "train_model"),
        os.path.join(script_dir, "demo"),
    ]
    for d in candidates:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"{filename} not found near {script_dir}")


# --- data loading -----------------------------------------------------------------------------------------------

def load_data():
    # 1024-dim GluFormer embeddings
    filepath = _find("GluFormer_Representations_Shanghai_2023.csv")
    repr_df = pd.read_csv(filepath, index_col=0)
    repr_df.index = repr_df.index.map(normalize_participant_id)
    repr_df = repr_df.groupby(repr_df.index).mean()

    # GMI feature (single column)
    gmi_path = _find("Shanghai_GMI.csv")
    gmi_df = pd.read_csv(gmi_path, index_col=0)
    gmi_df.index = gmi_df.index.map(normalize_participant_id)
    gmi_df = gmi_df.groupby(gmi_df.index).mean()[["GMI"]]

    # HbA1c target
    result_path = _find("Shanghai_results.csv")
    targets = pd.read_csv(result_path, index_col=0).iloc[:, 0]
    targets = targets[~targets.isna()]
    targets.index = targets.index.map(normalize_participant_id)
    targets = targets.groupby(targets.index).mean()

    return repr_df, gmi_df, targets


# --- EVOLVE-BLOCK-START
def build_features_and_predict(repr_train, gmi_train, y_train, repr_test,  gmi_test):
    """
    Given per-fold train/test splits of both feature sources,
    build features and return predictions for the test set.

    Targets to optimise: Pearson correlation with HbA1c (higher is better)
      A. Feature selection: which data to use and how to combine it
         - repr: 1024-dim GluFormer embeddings (rich but high-dimensional)
         - gmi:  1-dim GMI value (simple clinical proxy for mean glucose)
         - both: concatenated [repr | gmi]
      B. Predictor: model class and hyperparameters
    """
    # Feature selection — baseline: Representation only
    X_train = repr_train
    X_test  = repr_test

    # Predictor — baseline: Ridge, alpha=80, no scaling
    model = Ridge(alpha=80)
    model.fit(X_train, y_train)
    return model.predict(X_test)
# --- EVOLVE-BLOCK-END


# --- CV harness -----------------------------------------------------------------------------------------------

def run_cv(repr_df, gmi_df, targets, n_seeds=10, n_folds=5):
    ids = repr_df.index.intersection(gmi_df.index).intersection(targets.index)
    repr_df = repr_df.loc[ids]
    gmi_df  = gmi_df.loc[ids]
    targets = targets.loc[ids]
    ids     = ids.values
 
    pearson_per_seed  = []
    spearman_per_seed = []
 
    for seed in range(n_seeds):
        preds_all, targets_all = [], []
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=seed)
 
        for train_idx, test_idx in kf.split(np.unique(ids)):
            train_ids = ids[train_idx]
            test_ids  = ids[test_idx]
 
            repr_tr = repr_df.loc[train_ids].values
            gmi_tr  = gmi_df.loc[train_ids].values
            y_tr    = targets.loc[train_ids].values
 
            repr_te = repr_df.loc[test_ids].groupby(
                          repr_df.loc[test_ids].index).mean().values
            gmi_te  = gmi_df.loc[test_ids].groupby(
                          gmi_df.loc[test_ids].index).mean().values
            y_te    = targets.loc[test_ids].groupby(
                          targets.loc[test_ids].index).mean().values
 
            y_tr = (y_tr - y_tr.mean()) / y_tr.std()
 
            y_pred = build_features_and_predict(
                repr_tr, gmi_tr, y_tr,
                repr_te, gmi_te
            )
            preds_all.append(y_pred)
            targets_all.append(y_te)
 
        y_pred_all = np.concatenate(preds_all).squeeze()
        y_true_all = np.concatenate(targets_all).squeeze()
 
        pearson_per_seed.append(
            float(np.corrcoef(y_pred_all, y_true_all)[0, 1])
        )
        spearman_per_seed.append(
            float(spearmanr(y_pred_all, y_true_all).correlation)
        )
 
    pearson_r = float(np.mean(pearson_per_seed))
    spearman_r = float(np.mean(spearman_per_seed))
    # prediction_stability: 1 - normalised std of pearson across seeds
    # higher = more consistent predictions regardless of random CV split
    prediction_stability = float(1.0 - np.std(pearson_per_seed))
 
    combined_score = (
        pearson_r
        + 0.3 * spearman_r
        - 0.2 * (1.0 - prediction_stability)   # penalise instability
    )
 
    return {
        "combined_score":        round(combined_score,        6),
        "pearson_r":             round(pearson_r,             6),
        "spearman_r":            round(spearman_r,            6),
        "prediction_stability":  round(prediction_stability,  6),
    }
 
 
if __name__ == "__main__":
    repr_df, gmi_df, targets = load_data()
    results = run_cv(repr_df, gmi_df, targets)
    print("Metrics:")
    for k, v in results.items():
        print(f"  {k}: {v}")
