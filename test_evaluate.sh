#!/bin/bash

# Test script for /api/evaluate endpoint
# This endpoint evaluates mathematical expressions as strings

echo "Testing /api/evaluate endpoint on http://localhost:8080"
echo "=========================================="

# Valid expressions
echo -e "\n1. Simple addition (5 + 3):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "5 + 3"}'

echo -e "\n\n2. Simple subtraction (15 - 7):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "15 - 7"}'

echo -e "\n\n3. Simple multiplication (6 * 9):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "6 * 9"}'

echo -e "\n\n4. Simple division (100 / 4):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "100 / 4"}'

echo -e "\n\n5. Decimal numbers (3.14 * 2):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "3.14 * 2"}'

echo -e "\n\n6. Negative numbers (-5 + 10):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "-5 + 10"}'

echo -e "\n\n7. Division with decimals (7.5 / 2.5):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "7.5 / 2.5"}'

# Error cases
echo -e "\n\n8. Division by zero (should return error):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "10 / 0"}'

echo -e "\n\n9. Invalid expression format (should return error):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "5 +"}'

echo -e "\n\n10. Multiple operators (should return error):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "5 + 3 * 2"}'

echo -e "\n\n11. Invalid operator (should return error):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "5 % 2"}'

echo -e "\n\n12. Empty expression (should return error):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": ""}'

echo -e "\n\n13. Text instead of numbers (should return error):"
curl -X POST http://localhost:8080/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "five + three"}'

echo -e "\n"