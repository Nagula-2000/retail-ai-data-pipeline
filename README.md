# Retail AI Data Pipeline

A portfolio project demonstrating retail sales data ingestion, cleaning, quality validation, revenue reporting, and SQL analytics using **synthetic example data**.

> **Current scope:** ETL and analytics starter. ML stock-out prediction and AI capabilities are planned, not implemented yet.

## Project structure

```text
data/sample_sales.csv         Example input transactions
src/pipeline.py               Python ETL and validation
sql/retail_analysis.sql       Business analysis queries
tests/test_pipeline.py        Unit tests
.github/workflows/tests.yml   Automated test workflow
requirements.txt              Python dependencies
```

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.pipeline --input data/sample_sales.csv --output outputs
pytest -q
```

Outputs: `outputs/clean_sales.csv`, `outputs/rejected_sales.csv`, and `outputs/store_summary.csv`.

The pipeline drops duplicate transaction IDs (keeping the first), rejects missing or invalid values, computes `revenue = quantity * unit_price`, and aggregates revenue by store. Invalid records are saved separately for review. Duplicate rows are removed rather than included in rejected output.

## SQL

Load `outputs/clean_sales.csv` into a table named `clean_sales` in your SQL database and run `sql/retail_analysis.sql` for store and product revenue reports.

## Next steps

- Add more realistic synthetic multi-store data and additional quality checks
- Build a Power BI or Streamlit dashboard
- Add incremental ingestion and pipeline monitoring
- Explore stock-out prediction using appropriate inventory history

## Portfolio note

All data in this repository is synthetic; this project does not contain employer or customer records.
