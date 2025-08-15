#!/bin/bash

# Test script for /api/calculate endpoint
# This endpoint performs various mathematical operations

echo "Testing /api/calculate endpoint on http://localhost:8080"
echo "=========================================="

# Basic arithmetic operations
echo -e "\n1. Addition (5 + 3):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "+", "a": 5, "b": 3}'

echo -e "\n\n2. Subtraction (10 - 4):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "-", "a": 10, "b": 4}'

echo -e "\n\n3. Multiplication (7 * 6):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "*", "a": 7, "b": 6}'

echo -e "\n\n4. Division (20 / 4):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "/", "a": 20, "b": 4}'

# Scientific functions (single operand)
echo -e "\n\n5. Square root (√16):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "sqrt", "a": 16}'

echo -e "\n\n6. Sine (sin(0)):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "sin", "a": 0}'

echo -e "\n\n7. Cosine (cos(0)):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "cos", "a": 0}'

echo -e "\n\n8. Logarithm base 10 (log(100)):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "log", "a": 100}'

echo -e "\n\n9. Natural logarithm (ln(2.718281828)):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "ln", "a": 2.718281828}'

# Error cases
echo -e "\n\n10. Division by zero (should return error):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "/", "a": 10, "b": 0}'

echo -e "\n\n11. Square root of negative (should return error):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "sqrt", "a": -4}'

echo -e "\n\n12. Invalid operation (should return error):"
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "invalid", "a": 5, "b": 3}'

echo -e "\n"