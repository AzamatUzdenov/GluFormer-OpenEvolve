"""
evaluator.py
OpenEvolve evaluator for GluFormer HbA1c prediction.
"""

import importlib.util
import sys
import traceback


def evaluate(program_path: str) -> dict:
    try:
        spec = importlib.util.spec_from_file_location("evolved", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return {"combined_score": 0.0, "error": f"Import failed: {e}"}

    for fn in ["load_data", "run_cv", "build_features_and_predict"]:
        if not hasattr(module, fn):
            return {"combined_score": 0.0, "error": f"Missing: {fn}"}

    try:
        repr_df, gmi_df, targets = module.load_data()
        results = module.run_cv(repr_df, gmi_df, targets)

        if not isinstance(results, dict):
            return {"combined_score": 0.0,
                    "error": "run_cv() must return a dict"}

        if not (-2.0 <= results["combined_score"] <= 2.0):
            return {"combined_score": 0.0,
                    "error": f"combined_score out of range: {results['combined_score']}"}

        return results

    except Exception:
        return {"combined_score": 0.0,
                "error": traceback.format_exc()[-600:]}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "initial_program.py"
    result = evaluate(path)
    print("Evaluation result:")
    for k, v in result.items():
        print(f"  {k}: {v}")