import pytest
import json
import requests
import time
import os
from requests.exceptions import ConnectionError, Timeout


@pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Integration tests skipped in CI environment"
)
class TestRoutes:
    """Test suite for Flask Calculator API endpoints using real HTTP requests"""

    BASE_URL = "http://localhost:8080"
    TIMEOUT = 5  # seconds

    @classmethod
    def setup_class(cls):
        """Check if server is running before running tests"""
        try:
            response = requests.get(f"{cls.BASE_URL}/health", timeout=cls.TIMEOUT)
            if response.status_code == 200:
                print(f"\n✅ Server is running at {cls.BASE_URL}")
            else:
                pytest.exit(
                    f"❌ Server responded with status {response.status_code}. Please start the server first."
                )
        except ConnectionError:
            pytest.exit(
                f"❌ Cannot connect to server at {cls.BASE_URL}. Please start the server first.\n"
                f"   Run: ./docker-start.sh or python run.py"
            )
        except Timeout:
            pytest.exit(
                f"❌ Server at {cls.BASE_URL} is not responding. Please check server status."
            )
        except Exception as e:
            pytest.exit(f"❌ Error connecting to server: {str(e)}")

    def test_index(self):
        """Test the main page loads correctly"""
        response = requests.get(f"{self.BASE_URL}/")
        assert response.status_code == 200
        assert "Visual Calculator" in response.text

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "flask-calculator"
        assert "version" in data

    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = requests.get(f"{self.BASE_URL}/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "metrics" in data
        assert "note" in data

    def test_calculate_addition(self):
        """Test basic addition calculation"""
        payload = {"operation": "+", "a": 5, "b": 3}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8
        assert data["operation"] == "+"
        assert data["a"] == 5
        assert data["b"] == 3

    def test_calculate_division(self):
        """Test division calculation"""
        payload = {"operation": "/", "a": 10, "b": 2}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5

    def test_calculate_sqrt(self):
        """Test square root calculation"""
        payload = {"operation": "sqrt", "a": 16}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 4

    def test_calculate_missing_data(self):
        """Test error handling for missing data"""
        response = requests.post(
            f"{self.BASE_URL}/api/calculate",
            headers={"Content-Type": "application/json"},
            timeout=self.TIMEOUT,
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"] == "No data provided"

    def test_calculate_missing_parameters(self):
        """Test error handling for missing parameters"""
        payload = {"operation": "+"}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Missing required parameters" in data["error"]

    def test_calculate_invalid_numbers(self):
        """Test error handling for invalid number format"""
        payload = {"operation": "+", "a": "not_a_number", "b": 3}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Invalid number format" in data["error"]

    def test_calculate_division_by_zero(self):
        """Test error handling for division by zero"""
        payload = {"operation": "/", "a": 10, "b": 0}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Division by zero" in data["error"]

    def test_evaluate_expression(self):
        """Test basic expression evaluation"""
        payload = {"expression": "5 + 3"}
        response = requests.post(
            f"{self.BASE_URL}/api/evaluate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8
        assert data["expression"] == "5 + 3"

    def test_evaluate_missing_expression(self):
        """Test error handling for missing expression"""
        response = requests.post(
            f"{self.BASE_URL}/api/evaluate", json={}, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "No expression provided" in data["error"]

    def test_evaluate_invalid_expression(self):
        """Test error handling for invalid expression"""
        payload = {"expression": "not valid"}
        response = requests.post(
            f"{self.BASE_URL}/api/evaluate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    # Additional comprehensive API tests
    def test_calculate_subtraction(self):
        """Test subtraction calculation"""
        payload = {"operation": "-", "a": 10, "b": 4}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 6

    def test_calculate_multiplication(self):
        """Test multiplication calculation"""
        payload = {"operation": "*", "a": 7, "b": 6}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 42

    def test_calculate_scientific_functions(self):
        """Test scientific function calculations"""
        # Test sin(0)
        payload = {"operation": "sin", "a": 0}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0

        # Test cos(0)
        payload = {"operation": "cos", "a": 0}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1

        # Test log(100)
        payload = {"operation": "log", "a": 100}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert abs(data["result"] - 2) < 0.0001

    def test_calculate_error_cases(self):
        """Test error cases for calculations"""
        # Test square root of negative
        payload = {"operation": "sqrt", "a": -4}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

        # Test invalid operation
        payload = {"operation": "invalid", "a": 5, "b": 3}
        response = requests.post(
            f"{self.BASE_URL}/api/calculate", json=payload, timeout=self.TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_evaluate_comprehensive(self):
        """Test comprehensive expression evaluation"""
        test_cases = [
            ("15 - 7", 8),
            ("6 * 9", 54),
            ("100 / 4", 25),
            ("-5 + 10", 5),
            ("3.14 * 2", 6.28),
        ]

        for expression, expected in test_cases:
            payload = {"expression": expression}
            response = requests.post(
                f"{self.BASE_URL}/api/evaluate", json=payload, timeout=self.TIMEOUT
            )
            assert response.status_code == 200
            data = response.json()
            if isinstance(expected, float):
                assert abs(data["result"] - expected) < 0.01
            else:
                assert data["result"] == expected

    def test_evaluate_error_cases(self):
        """Test error cases for expression evaluation"""
        error_cases = [
            ("10 / 0", "Division by zero"),
            ("5 + 3 * 2", "Invalid expression"),
            ("", "No expression provided"),
        ]

        for expression, expected_error in error_cases:
            if expression:
                payload = {"expression": expression}
            else:
                payload = {"expression": ""}

            response = requests.post(
                f"{self.BASE_URL}/api/evaluate", json=payload, timeout=self.TIMEOUT
            )
            assert response.status_code == 400
            data = response.json()
            assert "error" in data
