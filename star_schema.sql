-- Delete the visit fact table first so the script can be run again safely.
DROP TABLE IF EXISTS fact_visit;
-- Delete the patient dimension if it already exists.
DROP TABLE IF EXISTS dim_patient;
-- Delete the doctor dimension if it already exists.
DROP TABLE IF EXISTS dim_doctor;
-- Delete the department dimension if it already exists.
DROP TABLE IF EXISTS dim_department;
-- Delete the diagnosis dimension if it already exists.
DROP TABLE IF EXISTS dim_diagnosis;
-- Delete the date dimension if it already exists.
DROP TABLE IF EXISTS dim_date;

-- Create the patient dimension containing descriptive patient information.
CREATE TABLE dim_patient (
    -- Create the warehouse-generated patient key.
    PatientKey INTEGER PRIMARY KEY,
    -- Store the operational patient identifier.
    PatientID TEXT NOT NULL UNIQUE,
    -- Store the patient's first name.
    FirstName TEXT NOT NULL,
    -- Store the patient's family name.
    LastName TEXT NOT NULL,
    -- Store the patient's gender.
    Gender TEXT NOT NULL,
    -- Store the patient's birth date.
    DateOfBirth TEXT NOT NULL,
    -- Store the patient's district.
    District TEXT NOT NULL
);

-- Create the doctor dimension containing doctor information.
CREATE TABLE dim_doctor (
    -- Create the warehouse-generated doctor key.
    DoctorKey INTEGER PRIMARY KEY,
    -- Store the doctor's name.
    DoctorName TEXT NOT NULL UNIQUE
);

-- Create the department dimension containing hospital department information.
CREATE TABLE dim_department (
    -- Create the warehouse-generated department key.
    DepartmentKey INTEGER PRIMARY KEY,
    -- Store the department name.
    DepartmentName TEXT NOT NULL UNIQUE
);

-- Create the diagnosis dimension containing diagnosis information.
CREATE TABLE dim_diagnosis (
    -- Create the warehouse-generated diagnosis key.
    DiagnosisKey INTEGER PRIMARY KEY,
    -- Store the diagnosis name.
    DiagnosisName TEXT NOT NULL UNIQUE
);

-- Create the date dimension containing calendar attributes.
CREATE TABLE dim_date (
    -- Store the date key in YYYYMMDD format.
    DateKey INTEGER PRIMARY KEY,
    -- Store the complete calendar date.
    FullDate TEXT NOT NULL UNIQUE,
    -- Store the year number.
    YearNumber INTEGER NOT NULL,
    -- Store the quarter number.
    QuarterNumber INTEGER NOT NULL,
    -- Store the month number.
    MonthNumber INTEGER NOT NULL,
    -- Store the month name.
    MonthName TEXT NOT NULL,
    -- Store the day name.
    DayName TEXT NOT NULL
);

-- Create the central visit fact table containing measurements and foreign keys.
CREATE TABLE fact_visit (
    -- Create the warehouse-generated visit fact key.
    VisitFactKey INTEGER PRIMARY KEY,
    -- Store the original visit identifier as a degenerate dimension.
    VisitID TEXT NOT NULL UNIQUE,
    -- Link each visit to one patient.
    PatientKey INTEGER NOT NULL,
    -- Link each visit to one doctor.
    DoctorKey INTEGER NOT NULL,
    -- Link each visit to one department.
    DepartmentKey INTEGER NOT NULL,
    -- Link each visit to one diagnosis.
    DiagnosisKey INTEGER NOT NULL,
    -- Link each visit to one calendar date.
    DateKey INTEGER NOT NULL,
    -- Store the patient's calculated age during the visit.
    PatientAge INTEGER,
    -- Store the patient's analytical age group.
    AgeGroup TEXT,
    -- Store the hospital stay length in days.
    LengthOfStayDays INTEGER NOT NULL,
    -- Store the visit treatment cost in Rwandan francs.
    TreatmentCostRWF REAL NOT NULL,
    -- Store the payment method.
    PaymentMethod TEXT NOT NULL,
    -- Store the visit outcome.
    Outcome TEXT NOT NULL,
    -- Enforce the patient relationship.
    FOREIGN KEY (PatientKey) REFERENCES dim_patient(PatientKey),
    -- Enforce the doctor relationship.
    FOREIGN KEY (DoctorKey) REFERENCES dim_doctor(DoctorKey),
    -- Enforce the department relationship.
    FOREIGN KEY (DepartmentKey) REFERENCES dim_department(DepartmentKey),
    -- Enforce the diagnosis relationship.
    FOREIGN KEY (DiagnosisKey) REFERENCES dim_diagnosis(DiagnosisKey),
    -- Enforce the date relationship.
    FOREIGN KEY (DateKey) REFERENCES dim_date(DateKey)
);

-- Create an index to make patient-based analysis faster.
CREATE INDEX idx_fact_visit_patient ON fact_visit(PatientKey);
-- Create an index to make date-based analysis faster.
CREATE INDEX idx_fact_visit_date ON fact_visit(DateKey);
-- Create an index to make department-based analysis faster.
CREATE INDEX idx_fact_visit_department ON fact_visit(DepartmentKey);

