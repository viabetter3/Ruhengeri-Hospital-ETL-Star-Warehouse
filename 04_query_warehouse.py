"""Run simple analytical SQL queries against the hospital star warehouse."""

# Import Path to locate the database file reliably.
from pathlib import Path
# Import sqlite3 to connect to the data warehouse.
import sqlite3
# Import pandas to display SQL results as readable tables.
import pandas as pd

# Store the project folder containing this Python file.
PROJECT_DIR = Path(__file__).resolve().parent
# Store the location of the hospital star warehouse.
DATABASE_FILE = PROJECT_DIR / "warehouse" / "hospital_star_warehouse.db"
# Open a connection to the warehouse database.
connection = sqlite3.connect(DATABASE_FILE)
# Write a star-schema query that summarizes visits and cost by department.
department_query = """
-- Select the department name from its dimension table.
SELECT d.DepartmentName,
       -- Count hospital visits in each department.
       COUNT(*) AS NumberOfVisits,
       -- Calculate the total treatment cost in each department.
       ROUND(SUM(f.TreatmentCostRWF), 0) AS TotalCostRWF,
       -- Calculate the average treatment cost in each department.
       ROUND(AVG(f.TreatmentCostRWF), 0) AS AverageCostRWF
-- Read measurements from the central fact table.
FROM fact_visit AS f
-- Join the department dimension using its surrogate key.
JOIN dim_department AS d ON f.DepartmentKey = d.DepartmentKey
-- Create one result row for each department.
GROUP BY d.DepartmentName
-- Display departments from the highest total cost to the lowest.
ORDER BY TotalCostRWF DESC;
"""
# Run the department query and store its results in a pandas table.
department_results = pd.read_sql_query(department_query, connection)
# Display a heading for the analytical results.
print("\nHOSPITAL PERFORMANCE BY DEPARTMENT")
# Display the results without pandas row numbers.
print(department_results.to_string(index=False))
# Close the warehouse connection after analysis.
connection.close()

