# CSV Data Structure Documentation

## Overview
This document describes the expected column structure for each CSV file used by the HR Assistant.

---

## 1. employee_data.csv

**Purpose:** Store employee personal and employment information

**Required Columns:**
- `EmpID` - Unique employee identifier (e.g., "10026")
- `FirstName` - Employee first name
- `LastName` - Employee last name
- `Title` - Job title/position
- `Department` or `DepartmentType` - Department name
- `BusinessUnit` - Business unit/division
- `ADEmail` - Employee email address
- `EmployeeStatus` - Current status (Active, Terminated, etc.)
- `Supervisor` - Manager/supervisor name

**Optional Columns:**
- `StartDate`, `ExitDate`, `DOB`, `State`, `GenderCode`, `RaceDesc`, `MaritalDesc`
- `EmployeeType`, `PayZone`, `EmployeeClassificationType`
- `Performance Score`, `Current Employee Rating`
- `JobFunctionDescription`, `LocationCode`, `Division`
- `TerminationType`, `TerminationDescription`

**Sample Row:**
```
EmpID,FirstName,LastName,Title,DepartmentType,ADEmail,EmployeeStatus
10026,Adinah,Burnham,Data Analyst,IT,adinah.burnham@company.com,Active
```

---

## 2. leave_balances.csv

**Purpose:** Track employee leave/vacation balances

**Required Columns:**
- `EmpID` - Employee ID (must match employee_data.csv)
- `FirstName` - Employee first name
- `LastName` - Employee last name
- `AnnualLeave` - Remaining annual/vacation days
- `SickLeave` - Remaining sick leave days
- `PersonalLeave` - Remaining personal days
- `LeaveYear` - Year these balances apply to

**Sample Row:**
```
EmpID,FirstName,LastName,AnnualLeave,SickLeave,PersonalLeave,LeaveYear
10026,Adinah,Burnham,12,8,3,2024
```

---

## 3. recruitment_data.csv

**Purpose:** Store job applicant information and interview questions

**Required Columns:**
- `Job Title` - Position being recruited for
- `Applicant ID` - Unique applicant identifier
- `First Name`, `Last Name` - Applicant name
- `Status` - Application status (Applied, Interviewed, Hired, Rejected)

**Optional Columns:**
- `Application Date`, `Gender`, `Date of Birth`
- `Phone Number`, `Email`, `Address`, `City`, `State`, `Zip Code`, `Country`
- `Education Level`, `Years of Experience`, `Desired Salary`

**Note:** For generating interview questions, the tool will extract unique job titles from this file.

**Sample Row:**
```
Applicant ID,Job Title,First Name,Last Name,Status,Years of Experience
A1001,Data Scientist,John,Doe,Interviewed,5
```

---

## 4. NOT YET IMPLEMENTED (Future Use)

### employee_engagement_survey_data.csv
Survey responses and engagement scores (no tools built yet)

### training_and_development_data.csv
Training programs and employee development records (no tools built yet)

---

## Column Mapping Strategy

The tools are designed to be flexible with column names. They will:

1. **Primary Match:** Look for exact column names (case-sensitive)
2. **Fallback Match:** Try common variations (e.g., "Emp_ID", "EmployeeID", "Employee_ID")
3. **Error Handling:** Provide clear error messages if required columns are missing

### Adding New CSV Files

To add new CSV files:
1. Place the file in the `data/` folder
2. Update this README with column structure
3. Create corresponding tool functions in `tools/`
4. Register tools in `agent/tools.py`

---

## Data Privacy & Security

⚠️ **Important:**
- These CSV files may contain sensitive employee data
- Never commit real employee data to version control
- Use `.gitignore` to exclude `data/*.csv` if needed
- For production, use encrypted databases instead of CSV files

---

## Validation

To validate your CSV structure, run:
```bash
python utils/csv_validator.py
```

This will check for:
- Required columns present
- Data types correct
- No duplicate employee IDs
- Cross-file consistency (e.g., EmpID exists in both employee_data and leave_balances)