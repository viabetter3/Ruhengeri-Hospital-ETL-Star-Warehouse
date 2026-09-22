# Hospital ETL and Star Data Warehouse Practical

This project teaches non-programmer students how to generate, transform, and load 50,000 synthetic hospital visit records into a star-schema data warehouse.

## Star schema

The central `fact_visit` table contains visit measurements. It connects to `dim_patient`, `dim_doctor`, `dim_department`, `dim_diagnosis`, and `dim_date`.

## Requirements

- Python 3.10 or later
- pandas
- NumPy
- SQLite, which is included with Python

## Windows commands

```bash
python -m pip install -r requirements.txt
python run_all.py
```

## macOS or Linux commands

```bash
python3 -m pip install -r requirements.txt
python3 run_all.py
```

## Run one stage at a time

```bash
python 01_generate_hospital_data.py
python 02_transform_hospital_data.py
python 03_load_star_warehouse.py
python 04_query_warehouse.py
```

## Outputs

- `data/raw/hospital_visits_raw_50000.csv`: 50,000 unclean source records
- `data/processed/hospital_visits_clean.csv`: transformed records
- `warehouse/hospital_star_warehouse.db`: SQLite star data warehouse

## Teaching sequence

1. Open the raw CSV and identify inconsistent values.
2. Run the transformation and compare the clean CSV with the raw CSV.
3. Study the dimension and fact tables in `star_schema.sql`.
4. Run the loader and check that `fact_visit` contains exactly 50,000 rows.
5. Change the query in `04_query_warehouse.py` to analyze visits by diagnosis, month, doctor, or outcome.

All data in this project is synthetic and must not be interpreted as real patient information.

## Validation status

The complete synthetic-data ETL pipeline has been executed end-to-end successfully in a clean test run. Generated raw data, processed data, and SQLite warehouse files are intentionally excluded from version control and are recreated by `python run_all.py`.
