from flask import Blueprint, render_template, jsonify, request, current_app
from app.calculator import Calculator
import structlog

main = Blueprint("main", __name__)
logger = structlog.get_logger()


@main.route("/")
def index():
    logger.info("Serving calculator homepage")
    return render_template("calculator.html")


@main.route("/health")
def health():
    return jsonify(
        {"status": "healthy", "service": "flask-calculator", "version": "1.0.0"}
    )


@main.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        operation = data.get("operation")
        a = data.get("a")
        b = data.get("b")

        if operation is None or a is None:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            a = float(a)
            b = float(b) if b is not None else None
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid number format"}), 400

        logger.info("Calculating", operation=operation, a=a, b=b)

        result = Calculator.calculate(operation, a, b)

        logger.info("Calculation successful", result=result)

        return jsonify({"result": result, "operation": operation, "a": a, "b": b})

    except ValueError as e:
        logger.warning("Calculation error", error=str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error("Unexpected error", error=str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@main.route("/api/evaluate", methods=["POST"])
def evaluate():
    try:
        data = request.get_json(force=True, silent=True)

        if not data or "expression" not in data:
            return jsonify({"error": "No expression provided"}), 400

        expression = data["expression"]
        logger.info("Evaluating expression", expression=expression)

        result = Calculator.evaluate_expression(expression)

        logger.info("Evaluation successful", result=result)

        return jsonify({"result": result, "expression": expression})

    except ValueError as e:
        logger.warning("Evaluation error", error=str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error("Unexpected error", error=str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
