"""
Unit Tests for HR Assistant Tools
Tests employee_tools.py functions with various scenarios
"""

import pytest
import pandas as pd
from pathlib import Path
import sys
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.employee_tools import (
    get_employee_details,
    check_leave_balance,
    generate_interview_questions,
    normalize_employee_id,
    load_csv_safe,
    validate_csv_exists
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_employee_ids():
    """Sample valid employee IDs from actual CSV"""
    return ["3989", "10026", "10196", "10088"]


@pytest.fixture
def sample_job_roles():
    """Sample job roles from recruitment data"""
    return ["Data Scientist", "Software Engineer", "Marketing Manager"]


@pytest.fixture
def invalid_employee_id():
    """An employee ID that doesn't exist"""
    return "99999"


# ============================================================================
# TEST: CSV FILE VALIDATION
# ============================================================================

class TestCSVValidation:
    """Test CSV file existence and loading"""
    
    def test_employee_data_exists(self):
        """Test that employee_data.csv exists"""
        assert validate_csv_exists("employee_data.csv"), "employee_data.csv not found"
    
    def test_leave_balances_exists(self):
        """Test that leave_balances.csv exists"""
        assert validate_csv_exists("leave_balances.csv"), "leave_balances.csv not found"
    
    def test_recruitment_data_exists(self):
        """Test that recruitment_data.csv exists"""
        assert validate_csv_exists("recruitment_data.csv"), "recruitment_data.csv not found"
    
    def test_load_valid_csv(self):
        """Test loading a valid CSV file"""
        df = load_csv_safe("employee_data.csv")
        assert df is not None, "Failed to load employee_data.csv"
        assert not df.empty, "employee_data.csv is empty"
    
    def test_load_invalid_csv(self):
        """Test loading a non-existent CSV file"""
        df = load_csv_safe("nonexistent.csv")
        assert df is None, "Should return None for non-existent file"


# ============================================================================
# TEST: EMPLOYEE ID NORMALIZATION
# ============================================================================

class TestEmployeeIDNormalization:
    """Test employee ID normalization function"""
    
    def test_normalize_string_id(self):
        """Test normalizing string employee ID"""
        assert normalize_employee_id("3989") == "3989"
    
    def test_normalize_integer_id(self):
        """Test normalizing integer employee ID"""
        assert normalize_employee_id(3989) == "3989"
    
    def test_normalize_whitespace(self):
        """Test normalizing ID with whitespace"""
        assert normalize_employee_id("  3989  ") == "3989"
    
    def test_normalize_mixed(self):
        """Test normalizing ID with mixed issues"""
        assert normalize_employee_id("  10026  ") == "10026"


# ============================================================================
# TEST: GET EMPLOYEE DETAILS
# ============================================================================

class TestGetEmployeeDetails:
    """Test get_employee_details function"""
    
    def test_get_valid_employee(self, sample_employee_ids):
        """Test retrieving details for a valid employee"""
        emp_id = sample_employee_ids[0]  # 3989
        result = get_employee_details(emp_id)
        
        assert result["success"] is True, "Should succeed for valid employee"
        assert result["employee_id"] == emp_id, "Should return correct employee ID"
        assert "first_name" in result, "Should include first_name"
        assert "last_name" in result, "Should include last_name"
        assert "full_name" in result, "Should include full_name"
        assert "email" in result, "Should include email"
        assert "title" in result, "Should include title"
    
    def test_get_invalid_employee(self, invalid_employee_id):
        """Test retrieving details for non-existent employee"""
        result = get_employee_details(invalid_employee_id)
        
        assert result["success"] is False, "Should fail for invalid employee"
        assert "error" in result, "Should include error message"
        assert invalid_employee_id in result["error"], "Error should mention the ID"
    
    def test_employee_has_required_fields(self, sample_employee_ids):
        """Test that employee result has all required fields"""
        result = get_employee_details(sample_employee_ids[0])
        
        required_fields = ["success", "employee_id", "first_name", "last_name", "full_name"]
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"
    
    def test_employee_full_name_format(self, sample_employee_ids):
        """Test that full_name is correctly formatted"""
        result = get_employee_details(sample_employee_ids[0])
        
        if result["success"]:
            expected_name = f"{result['first_name']} {result['last_name']}"
            assert result["full_name"] == expected_name, "full_name should be 'FirstName LastName'"
    
    def test_whitespace_in_employee_id(self):
        """Test that whitespace in employee ID is handled"""
        result = get_employee_details("  3989  ")
        
        assert result["success"] is True, "Should handle whitespace in ID"
        assert result["employee_id"] == "3989", "Should normalize ID"


# ============================================================================
# TEST: CHECK LEAVE BALANCE
# ============================================================================

class TestCheckLeaveBalance:
    """Test check_leave_balance function"""
    
    def test_check_valid_employee_leave(self):
        """Test checking leave balance for a valid employee"""
        result = check_leave_balance("10026")
        
        assert result["success"] is True, "Should succeed for valid employee"
        assert "employee_id" in result, "Should include employee_id"
        assert "annual_leave" in result, "Should include annual_leave"
        assert "sick_leave" in result, "Should include sick_leave"
        assert "personal_leave" in result, "Should include personal_leave"
        assert "total_leave" in result, "Should include total_leave"
    
    def test_check_invalid_employee_leave(self, invalid_employee_id):
        """Test checking leave balance for non-existent employee"""
        result = check_leave_balance(invalid_employee_id)
        
        assert result["success"] is False, "Should fail for invalid employee"
        assert "error" in result, "Should include error message"
    
    def test_leave_balance_types(self):
        """Test that leave balance values are numeric"""
        result = check_leave_balance("10026")
        
        if result["success"]:
            
            assert isinstance(result["annual_leave"], (int, float, np.integer)), "annual_leave should be numeric"
            assert isinstance(result["sick_leave"], (int, float, np.integer)), "sick_leave should be numeric"
            assert isinstance(result["personal_leave"], (int, float, np.integer)), "personal_leave should be numeric"
    
    def test_total_leave_calculation(self):
        """Test that total_leave is correctly calculated"""
        result = check_leave_balance("10026")
        
        if result["success"]:
            expected_total = result["annual_leave"] + result["sick_leave"] + result["personal_leave"]
            assert result["total_leave"] == expected_total, "total_leave should be sum of all leave types"
    
    def test_leave_balance_non_negative(self):
        """Test that leave balances are non-negative"""
        result = check_leave_balance("10026")
        
        if result["success"]:
            assert result["annual_leave"] >= 0, "annual_leave should be non-negative"
            assert result["sick_leave"] >= 0, "sick_leave should be non-negative"
            assert result["personal_leave"] >= 0, "personal_leave should be non-negative"


# ============================================================================
# TEST: GENERATE INTERVIEW QUESTIONS
# ============================================================================

class TestGenerateInterviewQuestions:
    """Test generate_interview_questions function"""
    
    def test_generate_for_valid_role(self, sample_job_roles):
        """Test generating questions for a valid job role"""
        role = sample_job_roles[0]  # "Data Scientist"
        result = generate_interview_questions(role)
        
        assert result["success"] is True, "Should succeed for valid role"
        assert "questions" in result, "Should include questions list"
        assert isinstance(result["questions"], list), "questions should be a list"
        assert len(result["questions"]) > 0, "Should return at least one question"
    
    def test_generate_default_number_questions(self):
        """Test that default generates 5 questions"""
        result = generate_interview_questions("Data Scientist")
        
        if result["success"]:
            assert result["num_questions"] == 5, "Should generate 5 questions by default"
            assert len(result["questions"]) == 5, "Should have 5 questions in list"
    
    def test_generate_custom_number_questions(self):
        """Test generating custom number of questions"""
        num = 3
        result = generate_interview_questions("Software Engineer", num_questions=num)
        
        if result["success"]:
            assert result["num_questions"] == num, f"Should generate {num} questions"
            assert len(result["questions"]) == num, f"Should have {num} questions in list"
    
    def test_generate_for_invalid_role(self):
        """Test generating questions for non-existent role"""
        result = generate_interview_questions("Nonexistent Job Title 12345")
        
        assert result["success"] is False, "Should fail for invalid role"
        assert "error" in result, "Should include error message"
    
    def test_questions_are_strings(self):
        """Test that all questions are strings"""
        result = generate_interview_questions("Data Scientist")
        
        if result["success"]:
            for question in result["questions"]:
                assert isinstance(question, str), "Each question should be a string"
                assert len(question) > 0, "Each question should be non-empty"
    
    def test_case_insensitive_role_matching(self):
        """Test that role matching is case-insensitive"""
        result1 = generate_interview_questions("Data Scientist")
        result2 = generate_interview_questions("data scientist")
        
        # Both should succeed (case-insensitive matching)
        assert result1["success"] is True or result2["success"] is True, \
            "Should handle case-insensitive role matching"
    
    def test_partial_role_matching(self):
        """Test that partial role names match"""
        result = generate_interview_questions("Scientist")
        
        # Should match "Data Scientist" if it exists
        if result["success"]:
            assert "scientist" in result["job_role"].lower(), \
                "Should match roles containing the search term"


# ============================================================================
# TEST: ERROR HANDLING
# ============================================================================

class TestErrorHandling:
    """Test error handling across all functions"""
    
    def test_empty_employee_id(self):
        """Test handling of empty employee ID"""
        result = get_employee_details("")
        assert result["success"] is False, "Should handle empty ID gracefully"
    
    def test_none_employee_id(self):
        """Test handling of None employee ID"""
        try:
            result = get_employee_details(None)
            # Should either succeed with normalization or fail gracefully
            assert "success" in result, "Should return a result dictionary"
        except Exception:
            pytest.fail("Should not raise exception for None input")
    
    def test_special_characters_in_id(self):
        """Test handling of special characters in employee ID"""
        result = get_employee_details("!@#$%")
        assert result["success"] is False, "Should fail for invalid characters"
    
    def test_empty_job_role(self):
        """Test handling of empty job role"""
        result = generate_interview_questions("")
        assert result["success"] is False, "Should handle empty role gracefully"


# ============================================================================
# TEST: DATA INTEGRITY
# ============================================================================

class TestDataIntegrity:
    """Test data integrity and consistency"""
    
    def test_employee_csv_has_required_columns(self):
        """Test that employee_data.csv has all required columns"""
        df = load_csv_safe("employee_data.csv")
        required_cols = ["EmpID", "FirstName", "LastName"]
        
        for col in required_cols:
            assert col in df.columns, f"Missing required column: {col}"
    
    def test_leave_csv_has_required_columns(self):
        """Test that leave_balances.csv has all required columns"""
        df = load_csv_safe("leave_balances.csv")
        required_cols = ["EmpID", "AnnualLeave", "SickLeave", "PersonalLeave"]
        
        for col in required_cols:
            assert col in df.columns, f"Missing required column: {col}"
    
    def test_recruitment_csv_has_required_columns(self):
        """Test that recruitment_data.csv has all required columns"""
        df = load_csv_safe("recruitment_data.csv")
        assert "Job Title" in df.columns, "Missing 'Job Title' column"
    
    def test_no_duplicate_employee_ids(self):
        """Test that there are no duplicate employee IDs"""
        df = load_csv_safe("employee_data.csv")
        duplicates = df["EmpID"].duplicated().sum()
        assert duplicates == 0, f"Found {duplicates} duplicate employee IDs"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])