"""Simple retail ETL: validate transactions, calculate revenue, export summaries."""
from pathlib import Path
import argparse
import pandas as pd

REQUIRED = ["transaction_id", "store_id", "date", "product", "quantity", "unit_price"]


def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return clean sales and rejected records (with rejection reasons)."""
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    sales = df[REQUIRED].copy()
    sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce")
    sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce")
    sales["date"] = pd.to_datetime(sales["date"], errors="coerce")
    sales = sales.drop_duplicates(subset=["transaction_id"], keep="first")
    invalid = (
        sales[["transaction_id", "store_id", "product"]].isna().any(axis=1)
        | sales["date"].isna()
        | sales["quantity"].isna()
        | sales["unit_price"].isna()
        | (sales["quantity"] <= 0)
        | (sales["unit_price"] < 0)
    )
    rejected = sales.loc[invalid].copy()
    rejected["rejection_reason"] = "Missing, invalid, or nonpositive transaction field"
    clean = sales.loc[~invalid].copy()
    clean["revenue"] = (clean["quantity"] * clean["unit_price"]).round(2)
    clean["date"] = clean["date"].dt.strftime("%Y-%m-%d")
    return clean, rejected


def run(input_path: str | Path, output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(input_path, dtype={"transaction_id": "string", "store_id": "string"})
    clean, rejected = transform(raw)
    clean.to_csv(output / "clean_sales.csv", index=False)
    rejected.to_csv(output / "rejected_sales.csv", index=False)
    summary = clean.groupby("store_id", as_index=False).agg(
        transactions=("transaction_id", "count"),
        total_revenue=("revenue", "sum"),
    )
    summary.to_csv(output / "store_summary.csv", index=False)
    print(f"Processed {len(raw)} rows: {len(clean)} valid, {len(rejected)} rejected; outputs in {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and summarize retail sales")
    parser.add_argument("--input", default="data/sample_sales.csv")
    parser.add_argument("--output", default="outputs")
    args = parser.parse_args()
    run(args.input, args.output)
