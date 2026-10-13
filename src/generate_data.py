"""Generate reproducible synthetic transactions for 500 stores."""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

PRODUCTS = [("Milk", 4.50), ("Bread", 3.25), ("Eggs", 5.00),
            ("Rice", 9.50), ("Apples", 2.25), ("Coffee", 12.00)]


def generate(path: str | Path, rows: int = 10000, stores: int = 500, seed: int = 42) -> None:
    if rows < 1 or stores < 1:
        raise ValueError("rows and stores must be positive")
    rng = random.Random(seed)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["transaction_id", "store_id", "date", "product", "quantity", "unit_price"])
        for i in range(rows):
            product, price = rng.choice(PRODUCTS)
            writer.writerow([
                f"T{i + 1:07d}", f"S{rng.randint(1, stores):03d}",
                (date(2026, 1, 1) + timedelta(days=rng.randint(0, 269))).isoformat(),
                product, rng.randint(1, 8), price,
            ])
    print(f"Generated {rows} synthetic transactions for up to {stores} stores at {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/synthetic_sales.csv")
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--stores", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate(args.output, args.rows, args.stores, args.seed)
