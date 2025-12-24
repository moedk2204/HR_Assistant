import pandas as pd
from pathlib import Path
import sys

# Define expectations for each file based on tools/employee_tools.py logic
EXPECTED_FILES = {
    "employee_data.csv": {
        "required_columns": ["EmpID", "FirstName", "LastName"],
        "optional_columns": [
            "Title", "DepartmentType", "BusinessUnit", "ADEmail", 
            "EmployeeStatus", "Supervisor", "StartDate", "EmployeeType"
        ]
    },
    "leave_balances.csv": {
        "required_columns": ["EmpID", "AnnualLeave", "SickLeave", "PersonalLeave"],
        "optional_columns": ["FirstName", "LastName", "LeaveYear"]
    },
    "recruitment_data.csv": {
        "required_columns": ["Job Title"],
        "optional_columns": []
    }
}

def validate_data_files():
    """
    Validates existence and schema of all required data files.
    """
    # Assuming this script is in the root or tools folder, data should be in ./data or ../data
    # We'll look relative to this script file
    current_dir = Path(__file__).parent
    
    # Try current directory first, then parent if we are in tools/
    data_path = current_dir / "data"
    if not data_path.exists():
        data_path = current_dir.parent / "data"
    
    print("="*60)
    print(f"DATA VALIDATION CHECK")
    print(f"Scanning directory: {data_path.absolute()}")
    print("="*60)

    if not data_path.exists():
        print(f"❌ CRITICAL ERROR: 'data' directory not found.")
        return

    all_passed = True

    for filename, requirements in EXPECTED_FILES.items():
        file_path = data_path / filename
        print(f"\n📄 Checking {filename}...", end=" ")
        
        if not file_path.exists():
            print(f"\n❌ FAILED: File exists check")
            print(f"   -> Expected at: {file_path}")
            all_passed = False
            continue
            
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Check required columns
            required = requirements["required_columns"]
            missing = [col for col in required if col not in df.columns]
            
            if missing:
                print(f"\n❌ FAILED: Missing required columns")
                print(f"   -> Missing: {missing}")
                all_passed = False
            else:
                print(f"✅ PASSED")
                print(f"   • Rows found: {len(df)}")
                print(f"   • Required columns: OK")
                
                # Check optional
                optional = requirements["optional_columns"]
                found_opt = [col for col in optional if col in df.columns]
                missing_opt = [col for col in optional if col not in df.columns]
                
                if missing_opt:
                    print(f"   • Note: Missing optional columns: {missing_opt} (This is fine)")
                
                # Data Integrity Checks
                issues = []
                
                # Check 1: Empty file
                if df.empty:
                    issues.append("File is empty (0 rows)")
                
                # Check 2: Null EmpIDs (if applicable)
                if "EmpID" in df.columns:
                    null_ids = df["EmpID"].isnull().sum()
                    if null_ids > 0:
                        issues.append(f"Found {null_ids} rows with missing EmpID")
                        
                    # Check duplicates
                    dupes = df["EmpID"].astype(str).duplicated().sum()
                    if dupes > 0:
                        issues.append(f"Found {dupes} duplicate EmpIDs")

                if issues:
                    print(f"   ⚠️ WARNINGS: {'; '.join(issues)}")
                else:
                    print(f"   • Data Integrity: Looks good")

        except Exception as e:
            print(f"\n❌ FAILED: Could not read file")
            print(f"   -> Error: {str(e)}")
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("✅ SUCCESS: All data files meet the requirements.")
        print("   You can confidently run the agent.")
    else:
        print("❌ STATUS: Validation Failed. Please fix the errors above.")
    print("="*60)

if __name__ == "__main__":
    validate_data_files()
