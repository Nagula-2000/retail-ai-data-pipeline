import pandas as pd
import pytest
from src.pipeline import transform


def test_transform_filters_invalid_and_duplicates():
    data = pd.DataFrame([
        {"transaction_id": "1", "store_id": "A", "date": "2026-09-01", "product": "Milk", "quantity": 2, "unit_price": 3},
        {"transaction_id": "1", "store_id": "A", "date": "2026-09-01", "product": "Milk", "quantity": 2, "unit_price": 3},
        {"transaction_id": "2", "store_id": "B", "date": "bad", "product": "Bread", "quantity": 1, "unit_price": 4},
    ])
    clean, rejected = transform(data)
    assert len(clean) == 1
    assert len(rejected) == 1
    assert clean.iloc[0]["revenue"] == 6


def test_missing_columns():
    with pytest.raises(ValueError, match="Missing required"):
        transform(pd.DataFrame({"store_id": ["A"]}))
