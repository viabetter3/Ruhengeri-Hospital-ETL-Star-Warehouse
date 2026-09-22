"""Create the SQLite star schema and load transformed hospital data into it."""

# Import Path to locate project files reliably.
from pathlib import Path
# Import sqlite3 to create and communicate with the SQL data warehouse.
import sqlite3
# Import pandas to prepare dimension and fact tables.
import pandas as pd

# Store the project folder containing this Python file.
PROJECT_DIR = Path(__file__).resolve().parent
# Store the path of the transformed hospital CSV file.
CLEAN_FILE = PROJECT_DIR / "data" / "processed" / "hospital_visits_clean.csv"
# Store the folder where the warehouse database will be created.
WAREHOUSE_DIR = PROJECT_DIR / "warehouse"
# Create the warehouse folder if it does not already exist.
WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
# Store the path of the SQLite warehouse database.
DATABASE_FILE = WAREHOUSE_DIR / "hospital_star_warehouse.db"
# Store the path of the SQL star-schema definition.
SCHEMA_FILE = PROJECT_DIR / "star_schema.sql"
# Read the cleaned hospital records into a pandas table.
data = pd.read_csv(CLEAN_FILE)
# Open a connection to the SQLite data warehouse.
connection = sqlite3.connect(DATABASE_FILE)
# Activate foreign-key validation in SQLite.
connection.execute("PRAGMA foreign_keys = ON;")
# Read the complete SQL star-schema script as text.
schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
# Run the SQL script to create all dimension and fact tables.
connection.executescript(schema_sql)

# Select one row for each unique patient to create the patient dimension.
dim_patient = data[["PatientID", "FirstName", "LastName", "Gender", "DateOfBirth", "District"]].drop_duplicates("PatientID").sort_values("PatientID").reset_index(drop=True)
# Create integer surrogate keys for the patient dimension.
dim_patient.insert(0, "PatientKey", range(1, len(dim_patient) + 1))
# Create the doctor dimension from unique doctor names.
dim_doctor = data[["DoctorName"]].drop_duplicates().sort_values("DoctorName").reset_index(drop=True)
# Create integer surrogate keys for the doctor dimension.
dim_doctor.insert(0, "DoctorKey", range(1, len(dim_doctor) + 1))
# Create the department dimension from unique department names.
dim_department = data[["Department"]].drop_duplicates().sort_values("Department").reset_index(drop=True)
# Rename the department column to match the SQL dimension table.
dim_department = dim_department.rename(columns={"Department": "DepartmentName"})
# Create integer surrogate keys for the department dimension.
dim_department.insert(0, "DepartmentKey", range(1, len(dim_department) + 1))
# Create the diagnosis dimension from unique diagnosis names.
dim_diagnosis = data[["Diagnosis"]].drop_duplicates().sort_values("Diagnosis").reset_index(drop=True)
# Rename the diagnosis column to match the SQL dimension table.
dim_diagnosis = dim_diagnosis.rename(columns={"Diagnosis": "DiagnosisName"})
# Create integer surrogate keys for the diagnosis dimension.
dim_diagnosis.insert(0, "DiagnosisKey", range(1, len(dim_diagnosis) + 1))
# Select one row for each calendar date to create the date dimension.
dim_date = data[["DateKey", "VisitDate", "VisitYear", "VisitQuarter", "VisitMonth", "VisitMonthName", "VisitDayName"]].drop_duplicates("DateKey").sort_values("DateKey").reset_index(drop=True)
# Rename date columns to match the SQL dimension table.
dim_date = dim_date.rename(columns={"VisitDate": "FullDate", "VisitYear": "YearNumber", "VisitQuarter": "QuarterNumber", "VisitMonth": "MonthNumber", "VisitMonthName": "MonthName", "VisitDayName": "DayName"})

# Load the patient dimension into its SQL table.
dim_patient.to_sql("dim_patient", connection, if_exists="append", index=False)
# Load the doctor dimension into its SQL table.
dim_doctor.to_sql("dim_doctor", connection, if_exists="append", index=False)
# Load the department dimension into its SQL table.
dim_department.to_sql("dim_department", connection, if_exists="append", index=False)
# Load the diagnosis dimension into its SQL table.
dim_diagnosis.to_sql("dim_diagnosis", connection, if_exists="append", index=False)
# Load the date dimension into its SQL table.
dim_date.to_sql("dim_date", connection, if_exists="append", index=False)

# Add patient surrogate keys to visits by matching operational patient identifiers.
fact_visit = data.merge(dim_patient[["PatientKey", "PatientID"]], on="PatientID", how="left")
# Add doctor surrogate keys to visits by matching doctor names.
fact_visit = fact_visit.merge(dim_doctor, on="DoctorName", how="left")
# Add department surrogate keys to visits by matching department names.
fact_visit = fact_visit.merge(dim_department, left_on="Department", right_on="DepartmentName", how="left")
# Add diagnosis surrogate keys to visits by matching diagnosis names.
fact_visit = fact_visit.merge(dim_diagnosis, left_on="Diagnosis", right_on="DiagnosisName", how="left")
# Select only the keys, measures, and descriptive transaction fields needed in the fact table.
fact_visit = fact_visit[["VisitID", "PatientKey", "DoctorKey", "DepartmentKey", "DiagnosisKey", "DateKey", "PatientAge", "AgeGroup", "LengthOfStayDays", "TreatmentCostRWF", "PaymentMethod", "Outcome"]]
# Create integer surrogate keys for the visit fact rows.
fact_visit.insert(0, "VisitFactKey", range(1, len(fact_visit) + 1))
# Load the 50,000 hospital visits into the central fact table.
fact_visit.to_sql("fact_visit", connection, if_exists="append", index=False)
# Save all completed database changes.
connection.commit()

# Create a list of warehouse tables that need record-count verification.
tables = ["dim_patient", "dim_doctor", "dim_department", "dim_diagnosis", "dim_date", "fact_visit"]
# Repeat the verification for each table in the list.
for table_name in tables:
    # Ask the database to count all records in the current table.
    record_count = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    # Display the table name and verified number of loaded records.
    print(f"{table_name}: {record_count:,} rows")

# Close the database connection after loading and verification.
connection.close()
# Display the path of the completed star data warehouse.
print(f"Warehouse created: {DATABASE_FILE}")

