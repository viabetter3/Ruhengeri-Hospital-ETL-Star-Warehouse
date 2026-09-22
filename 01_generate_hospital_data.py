"""Generate 50,000 synthetic hospital visit records for an ETL lesson."""

# Import Path so the program can create folders safely on any operating system.
from pathlib import Path
# Import NumPy to generate random numbers and select random values.
import numpy as np
# Import pandas to organize the generated records as a table and save them as CSV.
import pandas as pd

# Store the project folder containing this Python file.
PROJECT_DIR = Path(__file__).resolve().parent
# Store the folder where the raw source data will be saved.
RAW_DIR = PROJECT_DIR / "data" / "raw"
# Create the raw-data folder if it does not already exist.
RAW_DIR.mkdir(parents=True, exist_ok=True)
# Set the number of hospital visit records required by the exercise.
NUMBER_OF_RECORDS = 50_000
# Create a repeatable random-number generator so every class gets the same results.
rng = np.random.default_rng(2026)

# Create a small list of possible patient first names.
first_names = np.array(["Aline", "Beata", "Claude", "Diane", "Eric", "Fabrice", "Grace", "Henri", "Immaculee", "Jean"])
# Create a small list of possible patient family names.
last_names = np.array(["Uwimana", "Mugisha", "Mukamana", "Niyonzima", "Habimana", "Uwera", "Ishimwe", "Mutabazi", "Nshimiyimana", "Ingabire"])
# Create the hospital departments used in the example.
departments = np.array(["Emergency", "Cardiology", "Pediatrics", "Maternity", "Surgery", "Internal Medicine"])
# Create the doctor names used in the example.
doctors = np.array(["Dr. Alice", "Dr. Bosco", "Dr. Chantal", "Dr. David", "Dr. Esther", "Dr. Felix", "Dr. Grace", "Dr. Hugo"])
# Create the diagnoses used in the example.
diagnoses = np.array(["Malaria", "Diabetes", "Hypertension", "Pneumonia", "Fracture", "Gastritis", "Asthma", "Pregnancy care"])
# Create the available patient genders.
genders = np.array(["Male", "Female"])
# Create the available payment methods.
payment_methods = np.array(["Insurance", "Cash", "Mobile Money"])
# Create the available visit outcomes.
outcomes = np.array(["Discharged", "Admitted", "Referred"])

# Generate reusable patient identifiers so patients can have more than one visit.
patient_ids = np.array([f"P{number:05d}" for number in range(1, 10_001)])
# Generate 10,000 reusable patient first names.
patient_first_names = rng.choice(first_names, size=len(patient_ids))
# Generate 10,000 reusable patient family names.
patient_last_names = rng.choice(last_names, size=len(patient_ids))
# Generate 10,000 reusable patient genders.
patient_genders = rng.choice(genders, size=len(patient_ids))
# Generate 10,000 reusable patient birth dates.
patient_birth_dates = pd.to_datetime("1940-01-01") + pd.to_timedelta(rng.integers(0, 29_500, size=len(patient_ids)), unit="D")
# Generate 10,000 reusable patient districts.
patient_districts = rng.choice(np.array(["Gasabo", "Kicukiro", "Nyarugenge", "Musanze", "Huye", "Rubavu"]), size=len(patient_ids))
# Place reusable patient attributes in a lookup table.
patient_master = pd.DataFrame({"PatientID": patient_ids, "FirstName": patient_first_names, "LastName": patient_last_names, "Gender": patient_genders, "DateOfBirth": patient_birth_dates, "District": patient_districts})

# Select one patient identifier for each of the 50,000 visits.
visit_patient_ids = rng.choice(patient_ids, size=NUMBER_OF_RECORDS)
# Create the 50,000 visit rows with the selected patient identifiers.
hospital_data = pd.DataFrame({"VisitID": [f"V{number:06d}" for number in range(1, NUMBER_OF_RECORDS + 1)], "PatientID": visit_patient_ids})
# Add patient details to every visit by matching PatientID.
hospital_data = hospital_data.merge(patient_master, on="PatientID", how="left")
# Generate random visit dates from 1 January 2024 across approximately three years.
hospital_data["VisitDate"] = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 1_096, size=NUMBER_OF_RECORDS), unit="D")
# Generate a department for every visit.
hospital_data["Department"] = rng.choice(departments, size=NUMBER_OF_RECORDS)
# Generate a doctor for every visit.
hospital_data["DoctorName"] = rng.choice(doctors, size=NUMBER_OF_RECORDS)
# Generate a diagnosis for every visit.
hospital_data["Diagnosis"] = rng.choice(diagnoses, size=NUMBER_OF_RECORDS)
# Generate a stay length from zero to fourteen days for every visit.
hospital_data["LengthOfStayDays"] = rng.integers(0, 15, size=NUMBER_OF_RECORDS)
# Generate a treatment cost between RWF 5,000 and RWF 1,500,000 for every visit.
hospital_data["TreatmentCostRWF"] = rng.integers(5_000, 1_500_001, size=NUMBER_OF_RECORDS)
# Generate a payment method for every visit.
hospital_data["PaymentMethod"] = rng.choice(payment_methods, size=NUMBER_OF_RECORDS, p=[0.65, 0.20, 0.15])
# Generate a clinical outcome for every visit.
hospital_data["Outcome"] = rng.choice(outcomes, size=NUMBER_OF_RECORDS, p=[0.72, 0.20, 0.08])
# Add extra spaces to selected department values to create a realistic cleaning problem.
hospital_data.loc[hospital_data.index % 97 == 0, "Department"] = "  emergency  "
# Change selected diagnosis values to lowercase to create inconsistent capitalization.
hospital_data.loc[hospital_data.index % 113 == 0, "Diagnosis"] = "malaria"
# Insert missing payment methods into selected rows to demonstrate missing-value treatment.
hospital_data.loc[hospital_data.index % 211 == 0, "PaymentMethod"] = None
# Insert negative costs into selected rows to demonstrate invalid-value treatment.
hospital_data.loc[hospital_data.index % 307 == 0, "TreatmentCostRWF"] = -1000
# Define the full path of the raw CSV file.
output_file = RAW_DIR / "hospital_visits_raw_50000.csv"
# Save all 50,000 raw records without an extra spreadsheet index column.
hospital_data.to_csv(output_file, index=False)
# Display the number of generated records for the student.
print(f"Generated records: {len(hospital_data):,}")
# Display the location of the generated file for the student.
print(f"Raw file: {output_file}")

