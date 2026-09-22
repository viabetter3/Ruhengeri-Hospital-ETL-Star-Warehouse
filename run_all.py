"""Run the complete Extract, Transform, and Load pipeline in the correct order."""

# Import subprocess to run each classroom program as a separate step.
import subprocess
# Import sys to use the same Python interpreter that started this program.
import sys
# Import Path to locate all project scripts reliably.
from pathlib import Path

# Store the project folder containing this Python file.
PROJECT_DIR = Path(__file__).resolve().parent
# Store the scripts in the exact order required by the ETL pipeline.
scripts = ["01_generate_hospital_data.py", "02_transform_hospital_data.py", "03_load_star_warehouse.py", "04_query_warehouse.py"]
# Repeat the execution for every script in the ordered list.
for script_name in scripts:
    # Display the step that is about to run.
    print(f"\nRunning {script_name} ...")
    # Run the current script and stop immediately if that script reports an error.
    subprocess.run([sys.executable, str(PROJECT_DIR / script_name)], check=True)
# Display a final success message when all ETL steps finish.
print("\nThe complete hospital ETL pipeline finished successfully.")

