# Dashboard

The interactive dashboard reads the ETL output, not the raw CSV.

## Run

```bash
pip install -r requirements.txt
python -m src.pipeline
streamlit run dashboard/app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Features

- Filter by store and product
- Total revenue, unique transactions, and units sold
- Revenue over time
- Revenue by store and product
- Transaction details and rejected-row count

All example records are synthetic. No employer data is included.
