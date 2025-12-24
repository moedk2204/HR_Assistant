"""
LangChain Tool Registration
Wraps employee_tools functions for use with LangChain agents
"""

from langchain.tools import Tool
from typing import List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tools.employee_tools import (
    get_employee_details,
    check_leave_balance,
    generate_interview_questions,
    get_tool_schemas
)


def format_employee_details(result: dict) -> str:
    """Format employee details result for display"""
    if not result.get("success"):
        return f"❌ Error: {result.get('error', 'Unknown error')}"
    
    lines = [
        f"✓ Employee Found: {result['full_name']}",
        f"  • ID: {result['employee_id']}",
        f"  • Email: {result.get('email', 'N/A')}",
        f"  • Title: {result.get('title', 'N/A')}",
        f"  • Department: {result.get('department', 'N/A')}",
        f"  • Status: {result.get('status', 'N/A')}"
    ]
    
    if 'supervisor' in result:
        lines.append(f"  • Supervisor: {result['supervisor']}")
    if 'start_date' in result:
        lines.append(f"  • Start Date: {result['start_date']}")
    
    return "\n".join(lines)


def format_leave_balance(result: dict) -> str:
    """Format leave balance result for display"""
    if not result.get("success"):
        return f"❌ Error: {result.get('error', 'Unknown error')}"
    
    lines = [
        f"✓ Leave Balance for {result.get('employee_name', result['employee_id'])}:",
        f"  • Annual Leave: {result['annual_leave']} days",
        f"  • Sick Leave: {result['sick_leave']} days",
        f"  • Personal Leave: {result['personal_leave']} days",
        f"  • Total Available: {result['total_leave']} days"
    ]
    
    if 'leave_year' in result:
        lines.append(f"  • Year: {result['leave_year']}")
    
    return "\n".join(lines)


def format_interview_questions(result: dict) -> str:
    """Format interview questions result for display"""
    if not result.get("success"):
        return f"❌ Error: {result.get('error', 'Unknown error')}"
    
    lines = [
        f"✓ Interview Questions for {result['job_role']}:",
        f"  (Based on {result['based_on_applicants']} applicants)",
        ""
    ]
    
    for i, question in enumerate(result['questions'], 1):
        lines.append(f"  {i}. {question}")
    
    return "\n".join(lines)

# Wrapper functions with input cleaning
def get_employee_details_wrapper(employee_id: str) -> str:
    """Wrapper that cleans employee_id input"""
    # Clean input - remove trailing garbage
    employee_id = str(employee_id).strip()
    if '\n' in employee_id:
        employee_id = employee_id.split('\n')[0]
    if 'Question:' in employee_id:
        employee_id = employee_id.split('Question:')[0]
    if 'Thought:' in employee_id:
        employee_id = employee_id.split('Thought:')[0]
    employee_id = employee_id.strip()
    
    result = get_employee_details(employee_id)
    return format_employee_details(result)


def check_leave_balance_wrapper(employee_id: str) -> str:
    """Wrapper that cleans employee_id input"""
    # Clean input - remove trailing garbage
    employee_id = str(employee_id).strip()
    if '\n' in employee_id:
        employee_id = employee_id.split('\n')[0]
    if 'Question:' in employee_id:
        employee_id = employee_id.split('Question:')[0]
    if 'Thought:' in employee_id:
        employee_id = employee_id.split('Thought:')[0]
    employee_id = employee_id.strip()
    
    result = check_leave_balance(employee_id)
    return format_leave_balance(result)


def generate_interview_questions_wrapper(job_role: str) -> str:
    """Wrapper that cleans job_role input"""
    # Clean input - remove trailing garbage
    job_role = str(job_role).strip()
    if '\n' in job_role:
        job_role = job_role.split('\n')[0]
    if 'Question:' in job_role:
        job_role = job_role.split('Question:')[0]
    if 'Thought:' in job_role:
        job_role = job_role.split('Thought:')[0]
    job_role = job_role.strip()
    
    result = generate_interview_questions(job_role)
    return format_interview_questions(result)

def create_langchain_tools() -> List[Tool]:
    """
    Create LangChain Tool objects for all HR assistant functions
    
    Returns:
        List[Tool]: LangChain tools ready for agent use
    """
    tools = [
    Tool(
        name="get_employee_details",
        func=get_employee_details_wrapper,
        description=(
            "Retrieve detailed information about an employee including name, "
            "title, department, email, status, supervisor, and more. "
            "Input should be the employee ID (e.g., '10026')."
        )
    ),
    Tool(
        name="check_leave_balance",
        func=check_leave_balance_wrapper,
        description=(
            "Check an employee's remaining leave balance including annual leave, "
            "sick leave, and personal leave days. "
            "Input should be the employee ID (e.g., '10026')."
        )
    ),
    Tool(
        name="generate_interview_questions",
        func=generate_interview_questions_wrapper,
        description=(
            "Generate relevant interview questions for a specific job role. "
            "Input should be the job title (e.g., 'Data Scientist', 'Software Engineer'). "
            "Returns 5 thoughtful interview questions tailored to the role."
        )
    )
]
    
    return tools


def get_tool_descriptions() -> str:
    """Get a formatted string describing all available tools"""
    descriptions = [
        "Available HR Assistant Tools:",
        "",
        "1. get_employee_details - Get full employee information by ID",
        "2. check_leave_balance - Check remaining leave days for an employee",
        "3. generate_interview_questions - Create interview questions for a job role",
        "",
        "Use these tools to answer specific HR queries accurately."
    ]
    return "\n".join(descriptions)


if __name__ == "__main__":
    # Test tool creation
    tools = create_langchain_tools()
    print(f"✓ Created {len(tools)} LangChain tools")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:60]}...")