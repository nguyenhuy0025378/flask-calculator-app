import pytest
from app.calculator import Calculator


class TestCalculatorUnit:
    """Unit tests for Calculator class that don't require a live server"""

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        assert Calculator.calculate("+", 5, 3) == 8
        assert Calculator.calculate("-", 10, 4) == 6
        assert Calculator.calculate("*", 7, 6) == 42
        assert Calculator.calculate("/", 20, 4) == 5

    def test_scientific_functions(self):
        """Test scientific functions"""
        import math

        assert Calculator.calculate("sqrt", 16) == 4
        assert Calculator.calculate("sin", 0) == 0
        assert Calculator.calculate("cos", 0) == 1
        assert abs(Calculator.calculate("log", 100) - 2) < 0.0001
        assert abs(Calculator.calculate("ln", math.e) - 1) < 0.0001

    def test_division_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ValueError, match="Division by zero"):
            Calculator.calculate("/", 10, 0)

    def test_square_root_negative(self):
        """Test square root of negative number raises error"""
        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            Calculator.calculate("sqrt", -4)

    def test_log_non_positive(self):
        """Test logarithm of non-positive number raises error"""
        with pytest.raises(
            ValueError, match="Cannot calculate logarithm of non-positive number"
        ):
            Calculator.calculate("log", -5)

        with pytest.raises(
            ValueError, match="Cannot calculate logarithm of non-positive number"
        ):
            Calculator.calculate("ln", 0)

    def test_invalid_operation(self):
        """Test invalid operation raises error"""
        with pytest.raises(ValueError, match="Unknown operation: invalid"):
            Calculator.calculate("invalid", 5, 3)

    def test_missing_operand(self):
        """Test missing operand for binary operations"""
        with pytest.raises(ValueError, match="Operation \\+ requires two operands"):
            Calculator.calculate("+", 5)

    def test_evaluate_expression_basic(self):
        """Test expression evaluation"""
        assert Calculator.evaluate_expression("5 + 3") == 8
        assert Calculator.evaluate_expression("15 - 7") == 8
        assert Calculator.evaluate_expression("6 * 9") == 54
        assert Calculator.evaluate_expression("100 / 4") == 25

    def test_evaluate_expression_with_decimals(self):
        """Test expression evaluation with decimal numbers"""
        assert Calculator.evaluate_expression("3.14 * 2") == 6.28
        assert Calculator.evaluate_expression("7.5 / 2.5") == 3.0

    def test_evaluate_expression_with_negatives(self):
        """Test expression evaluation with negative numbers"""
        assert Calculator.evaluate_expression("-5 + 10") == 5
        assert Calculator.evaluate_expression("10 - -5") == 15

    def test_evaluate_expression_division_by_zero(self):
        """Test expression evaluation division by zero"""
        with pytest.raises(ValueError, match="Division by zero"):
            Calculator.evaluate_expression("10 / 0")

    def test_evaluate_expression_invalid_format(self):
        """Test invalid expression format"""
        with pytest.raises(ValueError, match="Invalid expression format"):
            Calculator.evaluate_expression("5 +")

        with pytest.raises(ValueError, match="Invalid expression format"):
            Calculator.evaluate_expression(
                "5 + 3 * 2"
            )  # Multiple operators not supported
