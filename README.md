# Retail AI Data Pipeline

A portfolio project demonstrating retail sales ingestion, cleaning, quality validation, SQL analytics, and an interactive **Streamlit dashboard** using synthetic example data.

> **Current scope:** ETL, analytics, and dashboard. AI agents and ML stock-out prediction are planned, not implemented.

## Project structure

```text
data/sample_sales.csv         Synthetic input transactions
src/pipeline.py               Python ETL and validation
dashboard/app.py              Interactive Streamlit dashboard
dashboard/README.md           Dashboard guide
sql/retail_analysis.sql       SQL business queries
tests/test_pipeline.py        ETL unit tests
.github/workflows/tests.yml   Automated CI checks
requirements.txt              Dependencies
```

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.pipeline
pytest -q
streamlit run dashboard/app.py
```

The pipeline creates `outputs/clean_sales.csv`, `outputs/rejected_sales.csv`, and `outputs/store_summary.csv`. The dashboard reads these generated outputs; run the ETL before launching Streamlit.

The pipeline removes duplicate transaction IDs, rejects missing or invalid records, computes `revenue = quantity * unit_price`, and summarizes revenue by store. Duplicates are removed, not included in the rejected-record output.

## Dashboard

Filter by store and product, explore revenue trends, compare store and product performance, and inspect transactions. See [dashboard documentation](dashboard/README.md).

## SQL

Load `outputs/clean_sales.csv` into a SQL table named `clean_sales` and run `sql/retail_analysis.sql`.

## Planned enhancements

- Incremental ingestion and scheduling
- Inventory history and stock-out prediction

## Portfolio note

All records are synthetic; no employer or customer data is included.


## Synthetic 500-store data and monitoring

Generate a larger reproducible synthetic dataset, process it, and validate the results:

```bash
python -m src.generate_data --output data/synthetic_sales.csv --rows 10000 --stores 500
python -m src.pipeline --input data/synthetic_sales.csv --output outputs
python -m src.quality_report --input data/synthetic_sales.csv --output outputs
pytest -q
streamlit run dashboard/app.py
```

The quality command writes `outputs/quality_report.json` and exits with a nonzero status if checks fail. The default invalid-row threshold is 5%; adjust it using `--max-invalid-rate 0.10` for 10%. Duplicate transactions are counted separately from invalid rows.

A GitHub Actions workflow in `.github/workflows/pipeline-monitor.yml` is configured for weekly checks and manual runs. Inspect the repository's **Actions** tab for actual execution status. GitHub may delay scheduled workflows or disable them on inactive repositories.

The generated CSV and pipeline outputs are local working files, not committed datasets. Run the commands above to produce them.
