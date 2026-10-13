"""Create machine-readable pipeline quality metrics and enforce thresholds."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REQUIRED = ["transaction_id", "store_id", "date", "product", "quantity", "unit_price"]


def report(raw: pd.DataFrame, clean: pd.DataFrame, rejected: pd.DataFrame,
           max_invalid_rate: float = 0.05) -> dict:
    if not 0 <= max_invalid_rate <= 1:
        raise ValueError("max_invalid_rate must be between 0 and 1")
    missing = sorted(set(REQUIRED) - set(raw.columns))
    duplicate_count = int(raw["transaction_id"].duplicated().sum()) if "transaction_id" in raw else 0
    invalid_count = len(rejected)
    total = len(raw)
    invalid_rate = invalid_count / total if total else 0.0
    reconciled = (len(clean) + invalid_count + duplicate_count == total)
    status = "pass" if total > 0 and not missing and invalid_rate <= max_invalid_rate and reconciled else "fail"
    return {
        "status": status,
        "raw_rows": total,
        "clean_rows": len(clean),
        "rejected_rows": invalid_count,
        "duplicate_rows_removed": duplicate_count,
        "invalid_rate": round(invalid_rate, 6),
        "max_invalid_rate": max_invalid_rate,
        "missing_columns": missing,
        "row_counts_reconciled": reconciled,
    }


def run(input_path: str, output_dir: str, max_invalid_rate: float = 0.05) -> dict:
    output = Path(output_dir)
    raw = pd.read_csv(input_path)
    clean = pd.read_csv(output / "clean_sales.csv")
    rejected = pd.read_csv(output / "rejected_sales.csv")
    metrics = report(raw, clean, rejected, max_invalid_rate)
    metrics["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    output.mkdir(parents=True, exist_ok=True)
    (output / "quality_report.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_sales.csv")
    parser.add_argument("--output", default="outputs")
    parser.add_argument("--max-invalid-rate", type=float, default=0.05)
    args = parser.parse_args()
    metrics = run(args.input, args.output, args.max_invalid_rate)
    raise SystemExit(0 if metrics["status"] == "pass" else 1)
