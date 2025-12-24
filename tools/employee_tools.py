"""
HR Assistant Tool Functions
Implements callable tools for querying employee data, leave balances, and recruitment info
"""

import pandas as pd
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


# Path to data directory
DATA_DIR = Path(__file__).parent.parent / "data"


def validate_csv_exists(filename: str) -> bool:
    """Check if a CSV file exists in the data directory"""
    filepath = DATA_DIR / filename
    return filepath.exists()


def load_csv_safe(filename: str) -> Optional[pd.DataFrame]:
    """
    Safely load a CSV file with error handling
    Returns None if file doesn't exist or can't be read
    """
    filepath = DATA_DIR / filename
    try:
        if not filepath.exists():
            print(f"ERROR: {filename} not found in {DATA_DIR}")
            return None
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"ERROR loading {filename}: {str(e)}")
        return None


def normalize_employee_id(emp_id: str) -> str:
    """
    Normalize employee ID for comparison
    Strips whitespace and converts to string
    """
    return str(emp_id).strip()


# ============================================================================
# TOOL 1: Get Employee Details
# ============================================================================

def get_employee_details(employee_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed information about an employee from employee_data.csv
    
    Args:
        employee_id (str): Employee ID (e.g., "10026", "10084")
    
    Returns:
        dict: Employee details including name, title, department, email, status
              Returns error dict if employee not found or CSV missing
    
    Example:
        >>> get_employee_details("10026")
        {
            "success": True,
            "employee_id": "10026",
            "first_name": "Adinah",
            "last_name": "Burnham",
            "full_name": "Adinah Burnham",
            "title": "Data Analyst",
            "department": "IT",
            "business_unit": "Technology",
            "email": "adinah.burnham@company.com",
            "status": "Active",
            "supervisor": "John Smith",
            "start_date": "2020-01-15",
            "employee_type": "Full-Time"
        }
    """
    # Normalize input
    emp_id = normalize_employee_id(employee_id)
    
    # Load CSV
    df = load_csv_safe("employee_data.csv")
    if df is None:
        return {
            "success": False,
            "error": "employee_data.csv not found or could not be loaded",
            "employee_id": emp_id
        }
    
    # Validate required columns
    required_cols = ["EmpID", "FirstName", "LastName"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return {
            "success": False,
            "error": f"Missing required columns in employee_data.csv: {missing_cols}",
            "employee_id": emp_id
        }
    
    # Convert EmpID to string for comparison
    df["EmpID"] = df["EmpID"].astype(str)
    
    # Find employee
    employee = df[df["EmpID"] == emp_id]
    
    if employee.empty:
        # Try to provide helpful feedback
        available_ids = df["EmpID"].head(5).tolist()
        return {
            "success": False,
            "error": f"Employee ID '{emp_id}' not found",
            "employee_id": emp_id,
            "hint": f"Sample valid IDs: {available_ids}"
        }
    
    # Extract employee data (first match)
    emp = employee.iloc[0]
    
    # Build response with available fields
    result = {
        "success": True,
        "employee_id": emp["EmpID"],
        "first_name": emp["FirstName"],
        "last_name": emp["LastName"],
        "full_name": f"{emp['FirstName']} {emp['LastName']}"
    }
    
    # Add optional fields if they exist
    optional_fields = {
        "Title": "title",
        "DepartmentType": "department",
        "BusinessUnit": "business_unit",
        "ADEmail": "email",
        "EmployeeStatus": "status",
        "Supervisor": "supervisor",
        "StartDate": "start_date",
        "EmployeeType": "employee_type",
        "Division": "division",
        "JobFunctionDescription": "job_function",
        "Performance Score": "performance_score",
        "Current Employee Rating": "current_rating"
    }
    
    for csv_col, result_key in optional_fields.items():
        if csv_col in df.columns and pd.notna(emp.get(csv_col)):
            result[result_key] = emp[csv_col]
    
    return result


# ============================================================================
# TOOL 2: Check Leave Balance
# ============================================================================

def check_leave_balance(employee_id: str) -> Dict[str, Any]:
    """
    Check the leave balance for an employee from leave_balances.csv
    
    Args:
        employee_id (str): Employee ID (e.g., "10026", "10084")
    
    Returns:
        dict: Leave balance details including annual, sick, and personal leave
              Returns error dict if employee not found or CSV missing
    
    Example:
        >>> check_leave_balance("10026")
        {
            "success": True,
            "employee_id": "10026",
            "employee_name": "Adinah Burnham",
            "annual_leave": 12,
            "sick_leave": 8,
            "personal_leave": 3,
            "total_leave": 23,
            "leave_year": 2024
        }
    """
    # Normalize input
    emp_id = normalize_employee_id(employee_id)
    
    # Load CSV
    df = load_csv_safe("leave_balances.csv")
    if df is None:
        return {
            "success": False,
            "error": "leave_balances.csv not found or could not be loaded",
            "employee_id": emp_id
        }
    
    # Validate required columns
    required_cols = ["EmpID", "AnnualLeave", "SickLeave", "PersonalLeave"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return {
            "success": False,
            "error": f"Missing required columns in leave_balances.csv: {missing_cols}",
            "employee_id": emp_id
        }
    
    # Convert EmpID to string for comparison
    df["EmpID"] = df["EmpID"].astype(str)
    
    # Find employee
    employee = df[df["EmpID"] == emp_id]
    
    if employee.empty:
        available_ids = df["EmpID"].head(5).tolist()
        return {
            "success": False,
            "error": f"Employee ID '{emp_id}' not found in leave records",
            "employee_id": emp_id,
            "hint": f"Sample valid IDs: {available_ids}"
        }
    
    # Extract leave data (first match)
    emp = employee.iloc[0]
    
    # Calculate total leave
    annual = emp["AnnualLeave"] if pd.notna(emp["AnnualLeave"]) else 0
    sick = emp["SickLeave"] if pd.notna(emp["SickLeave"]) else 0
    personal = emp["PersonalLeave"] if pd.notna(emp["PersonalLeave"]) else 0
    total = annual + sick + personal
    
    # Build response
    result = {
        "success": True,
        "employee_id": emp["EmpID"],
        "annual_leave": annual,
        "sick_leave": sick,
        "personal_leave": personal,
        "total_leave": total
    }
    
    # Add optional fields
    if "FirstName" in df.columns and "LastName" in df.columns:
        result["employee_name"] = f"{emp['FirstName']} {emp['LastName']}"
    
    if "LeaveYear" in df.columns and pd.notna(emp.get("LeaveYear")):
        result["leave_year"] = emp["LeaveYear"]
    
    return result


# ============================================================================
# TOOL 3: Generate Interview Questions
# ============================================================================

def generate_interview_questions(job_role: str, num_questions: int = 5) -> Dict[str, Any]:
    """
    Generate interview questions for a specific job role based on recruitment_data.csv
    
    Args:
        job_role (str): Job title/role (e.g., "Data Scientist", "Software Engineer")
        num_questions (int): Number of questions to generate (default: 5)
    
    Returns:
        dict: Interview questions and metadata
    """
    # Normalize input
    role = job_role.strip()

    if not role:
        return {
            "success": False,
            "error": "Job role cannot be empty",
            "job_role": job_role
        }
    
    # Load CSV
    df = load_csv_safe("recruitment_data.csv")
    if df is None:
        return {"success": False, "error": "recruitment_data.csv not found", "job_role": role}

    # Get unique job titles for matching
    available_roles = df["Job Title"].dropna().unique().tolist()
    matched_roles = [r for r in available_roles if role.lower() in r.lower() or r.lower() in role.lower()]
    if not matched_roles:
        return {"success": False, "error": f"Job role '{role}' not found", "job_role": role}

    # Use the best match
    best_match = matched_roles[0]
    
    # Count applicants for this role
    role_applicants = df[df["Job Title"] == best_match]
    num_applicants = len(role_applicants)

    # Generate role-specific interview questions
    questions_bank = generate_questions_for_role(best_match, num_questions)

    # Return as a proper dict so the agent can parse it correctly
    return {
        "success": True,
        "job_role": best_match,
        "original_query": role if role != best_match else None,
        "questions": questions_bank,
        "num_questions": len(questions_bank),
        "based_on_applicants": num_applicants
    }



def generate_questions_for_role(job_role: str, num_questions: int = 5) -> Dict[str, Any]:
    """
    Generate interview questions based on job role keywords
    This is a simple template system; production would use LLM or curated question bank
    """
    role = job_role.strip()
    role_lower = role.lower()
    
    if not role:
        return {
            "success": False,
            "error": "Job role cannot be empty",
            "job_role": job_role
        }
    
    # Common questions for all roles
    common_questions = [
        f"Tell me about your experience relevant to the {role} position.",
        f"What interests you most about this {role} role?",
        f"Describe a challenging project you've worked on in your career.",
        "How do you handle tight deadlines and pressure?",
        "Where do you see yourself in 5 years?"
    ]
    
    # Role-specific question templates
    role_specific = {
        "data": [
            "Explain your experience with data analysis and visualization tools.",
            "How do you ensure data quality and accuracy in your work?",
            "Describe your approach to handling large datasets.",
            "What statistical methods are you most comfortable with?",
            "How do you communicate complex data insights to non-technical stakeholders?"
        ],
        "scientist": [
            "Walk me through your experience with machine learning algorithms.",
            "How do you approach feature engineering and model selection?",
            "Describe a time when your model didn't perform as expected. What did you do?",
            "What's your experience with A/B testing and experimentation?",
            "How do you stay current with the latest developments in data science?"
        ],
        "engineer": [
            "Describe your software development process from requirements to deployment.",
            "How do you approach debugging complex technical issues?",
            "What's your experience with version control and collaborative coding?",
            "Tell me about a time you optimized code for better performance.",
            "How do you ensure code quality and maintainability?"
        ],
        "manager": [
            "Describe your leadership and team management style.",
            "How do you handle conflict within your team?",
            "What's your approach to performance reviews and feedback?",
            "How do you prioritize competing projects and resources?",
            "Tell me about a time you had to make a difficult personnel decision."
        ],
        "analyst": [
            "How do you approach problem-solving and root cause analysis?",
            "Describe your experience creating reports and dashboards.",
            "What tools and methodologies do you use for analysis?",
            "How do you validate your analytical findings?",
            "Give an example of how your analysis drove business decisions."
        ],
        "developer": [
            "What programming languages and frameworks are you most proficient in?",
            "How do you approach testing and quality assurance?",
            "Describe your experience with APIs and integrations.",
            "What's your approach to learning new technologies?",
            "Tell me about a technically challenging feature you've built."
        ]
    }
    
    # Select appropriate questions based on role keywords
    selected_questions = []
    
    # Add role-specific questions
    for keyword, questions in role_specific.items():
        if keyword in role_lower:
            selected_questions.extend(questions)
    
    # Add common questions
    selected_questions.extend(common_questions)
    
    # Remove duplicates and limit to requested number
    unique_questions = list(dict.fromkeys(selected_questions))
    
    return unique_questions[:num_questions] # type: ignore


# ============================================================================
# Utility Functions for Tool Registration
# ============================================================================

def get_tool_schemas() -> List[Dict[str, Any]]:
    """
    Return JSON schemas for all tools (for LangChain registration)
    """
    return [
        {
            "name": "get_employee_details",
            "description": "Retrieve detailed information about an employee including name, title, department, email, status, and more. Use this when asked about employee information, details, or profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID (e.g., '10026', '10084')"
                    }
                },
                "required": ["employee_id"]
            }
        },
        {
            "name": "check_leave_balance",
            "description": "Check an employee's remaining leave balance including annual leave, sick leave, and personal leave days. Use this when asked about vacation days, leave balance, or time off.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID (e.g., '10026', '10084')"
                    }
                },
                "required": ["employee_id"]
            }
        },
        {
            "name": "generate_interview_questions",
            "description": "Generate relevant interview questions for a specific job role based on recruitment data. Use this when asked to prepare interview questions or help with interviewing candidates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_role": {
                        "type": "string",
                        "description": "The job title or role (e.g., 'Data Scientist', 'Software Engineer')"
                    },
                    "num_questions": {
                        "type": "integer",
                        "description": "Number of questions to generate (default: 5)",
                        "default": 5
                    }
                },
                "required": ["job_role"]
            }
        }
    ]


# ============================================================================
# Tool Registry (for easy access)
# ============================================================================

AVAILABLE_TOOLS = {
    "get_employee_details": get_employee_details,
    "check_leave_balance": check_leave_balance,
    "generate_interview_questions": generate_interview_questions
}


def get_tool_by_name(tool_name: str):
    """Get a tool function by name"""
    return AVAILABLE_TOOLS.get(tool_name)