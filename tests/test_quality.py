import pandas as pd
import pytest

from src.generate_data import generate
from src.pipeline import run as run_pipeline
from src.quality_report import report


def test_generated_data_is_reproducible(tmp_path):
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"
    generate(first, rows=120, stores=12, seed=7)
    generate(second, rows=120, stores=12, seed=7)
    assert first.read_bytes() == second.read_bytes()
    output = tmp_path / "processed"
    run_pipeline(first, output)
    clean = pd.read_csv(output / "clean_sales.csv")
    rejected = pd.read_csv(output / "rejected_sales.csv")
    metrics = report(pd.read_csv(first), clean, rejected)
    assert metrics["status"] == "pass"
    assert metrics["raw_rows"] == 120


def test_quality_threshold_and_reconciliation():
    raw = pd.DataFrame({"transaction_id": ["1", "2", "3"]})
    clean = pd.DataFrame({"transaction_id": ["1", "2"]})
    rejected = pd.DataFrame({"transaction_id": ["3"]})
    metrics = report(raw, clean, rejected, max_invalid_rate=0.05)
    assert metrics["status"] == "fail"
    assert metrics["rejected_rows"] == 1


def test_invalid_threshold():
    with pytest.raises(ValueError):
        report(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), 2)
