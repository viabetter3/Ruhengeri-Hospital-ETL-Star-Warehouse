"""Clean and transform the 50,000 raw hospital visit records."""

# Import Path to create reliable file paths.
from pathlib import Path
# Import pandas to read, clean, transform, and save tabular data.
import pandas as pd

# Store the project folder containing this Python file.
PROJECT_DIR = Path(__file__).resolve().parent
# Store the path of the raw input CSV file.
RAW_FILE = PROJECT_DIR / "data" / "raw" / "hospital_visits_raw_50000.csv"
# Store the folder for cleaned data.
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
# Create the processed-data folder if it does not already exist.
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
# Read the raw hospital CSV file into a pandas table.
data = pd.read_csv(RAW_FILE)
# Display the raw record count before transformation.
print(f"Raw records read: {len(data):,}")

# Remove repeated rows if the source contains exact duplicates.
data = data.drop_duplicates()
# Remove spaces before and after all department names.
data["Department"] = data["Department"].str.strip()
# Convert department names to consistent title capitalization.
data["Department"] = data["Department"].str.title()
# Remove spaces before and after all diagnosis names.
data["Diagnosis"] = data["Diagnosis"].str.strip()
# Convert diagnosis names to consistent title capitalization.
data["Diagnosis"] = data["Diagnosis"].str.title()
# Replace missing payment methods with the word Unknown.
data["PaymentMethod"] = data["PaymentMethod"].fillna("Unknown")
# Convert visit dates from text into real date values.
data["VisitDate"] = pd.to_datetime(data["VisitDate"], errors="coerce")
# Convert patient birth dates from text into real date values.
data["DateOfBirth"] = pd.to_datetime(data["DateOfBirth"], errors="coerce")
# Convert treatment cost values to numbers and turn unreadable values into missing values.
data["TreatmentCostRWF"] = pd.to_numeric(data["TreatmentCostRWF"], errors="coerce")
# Replace negative treatment costs with zero because negative hospital charges are invalid here.
data.loc[data["TreatmentCostRWF"] < 0, "TreatmentCostRWF"] = 0
# Convert length-of-stay values to numbers and turn unreadable values into missing values.
data["LengthOfStayDays"] = pd.to_numeric(data["LengthOfStayDays"], errors="coerce")
# Replace missing length-of-stay values with zero.
data["LengthOfStayDays"] = data["LengthOfStayDays"].fillna(0)
# Convert length of stay into whole numbers.
data["LengthOfStayDays"] = data["LengthOfStayDays"].astype(int)
# Calculate completed patient years on the visit date and convert them to whole numbers.
data["PatientAge"] = ((data["VisitDate"] - data["DateOfBirth"]).dt.days // 365.25).astype("Int64")
# Create a date key in YYYYMMDD format for the date dimension.
data["DateKey"] = data["VisitDate"].dt.strftime("%Y%m%d").astype(int)
# Create the calendar year used in reporting.
data["VisitYear"] = data["VisitDate"].dt.year
# Create the calendar quarter used in reporting.
data["VisitQuarter"] = data["VisitDate"].dt.quarter
# Create the calendar month number used in reporting.
data["VisitMonth"] = data["VisitDate"].dt.month
# Create the full month name used in reporting.
data["VisitMonthName"] = data["VisitDate"].dt.month_name()
# Create the day name used in reporting.
data["VisitDayName"] = data["VisitDate"].dt.day_name()
# Create a simple age group for hospital analysis.
data["AgeGroup"] = pd.cut(data["PatientAge"], bins=[-1, 17, 35, 59, 200], labels=["0-17", "18-35", "36-59", "60+"])
# Convert transformed dates to standard ISO text before saving to CSV.
data["VisitDate"] = data["VisitDate"].dt.strftime("%Y-%m-%d")
# Convert birth dates to standard ISO text before saving to CSV.
data["DateOfBirth"] = data["DateOfBirth"].dt.strftime("%Y-%m-%d")
# Define the full path of the cleaned output CSV file.
output_file = PROCESSED_DIR / "hospital_visits_clean.csv"
# Save the transformed hospital records without an extra index column.
data.to_csv(output_file, index=False)
# Display the clean record count after transformation.
print(f"Clean records saved: {len(data):,}")
# Display the number of invalid negative costs remaining after cleaning.
print(f"Negative costs remaining: {(data['TreatmentCostRWF'] < 0).sum()}")
# Display the path of the transformed file.
print(f"Clean file: {output_file}")
