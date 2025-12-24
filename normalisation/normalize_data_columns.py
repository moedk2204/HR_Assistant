import pandas as pd
from pathlib import Path
import sys

# Define the TARGET schema we need
REQUIRED_SCHEMA = {
    "employee_data.csv": {
        "required": {
            "EmpID": ["id", "employee_id", "emp_id", "empid", "number", "employee_number"],
            "FirstName": ["first", "first_name", "firstname", "forename"],
            "LastName": ["last", "last_name", "lastname", "surname"]
        }
    },
    "leave_balances.csv": {
        "required": {
            "EmpID": ["id", "employee_id", "emp_id", "empid"],
            "AnnualLeave": ["annual", "vacation", "annual_leave", "vacation_days"],
            "SickLeave": ["sick", "sick_days", "sick_leave"],
            "PersonalLeave": ["personal", "personal_days", "personal_leave"]
        }
    }
}

def normalize_columns():
    current_dir = Path(__file__).parent
    data_path = current_dir / "data"
    
    if not data_path.exists():
        data_path = current_dir.parent / "data"

    print("="*60)
    print("CSV COLUMN NORMALIZER")
    print("="*60)

    for filename, schema in REQUIRED_SCHEMA.items():
        file_path = data_path / filename
        if not file_path.exists():
            print(f"Skipping {filename} (not found)")
            continue

        print(f"\nProcessing {filename}...")
        try:
            df = pd.read_csv(file_path)
            original_columns = list(df.columns)
            renamed = False
            
            # Check each required column
            for target_col, aliases in schema["required"].items():
                if target_col in df.columns:
                    print(f"  ✓ {target_col} already exists")
                    continue
                
                # Look for a match in aliases
                found = False
                for col in df.columns:
                    if col.lower() in aliases or col.lower().replace("_", "") in aliases:
                        print(f"  ↻ Auto-renaming '{col}' -> '{target_col}'")
                        df.rename(columns={col: target_col}, inplace=True)
                        renamed = True
                        found = True
                        break
                
                # If still not found, ask user
                if not found:
                    print(f"\n  ⚠️  MISSING: '{target_col}'")
                    print(f"     Available columns: {original_columns}")
                    user_input = input(f"     Type the column name to map to '{target_col}' (or press Enter to skip): ").strip()
                    if user_input and user_input in df.columns:
                        df.rename(columns={user_input: target_col}, inplace=True)
                        renamed = True
                        print(f"     Mapped '{user_input}' -> '{target_col}'")
            
            if renamed:
                backup_path = file_path.with_suffix('.csv.bak')
                print(f"\n  💾 Saving changes...")
                print(f"     Backup created at: {backup_path.name}")
                df.to_csv(backup_path, index=False) # Save backup just in case
                df.to_csv(file_path, index=False)   # Overwrite original
                print("     Done.")
            else:
                print("  ✓ No changes needed.")

        except Exception as e:
            print(f"  ❌ Error processing file: {e}")

if __name__ == "__main__":
    normalize_columns()
