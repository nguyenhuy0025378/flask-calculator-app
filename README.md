# Flask Calculator - MLOps Demo 0
 
## Features

- **Visual Calculator**: Web-based calculator with basic and scientific operations
- **RESTful API**: JSON API endpoints for calculations and expression evaluation
- **Structured Logging**: JSON-formatted logs with request tracking and correlation IDs
- **Metrics & Monitoring**: Basic metrics collection framework (ready for monitoring implementation)
- **Containerization**: Multi-stage Docker build with security best practices
- **Live Testing**: HTTP integration tests against running server with connectivity validation
- **CI/CD Ready**: GitHub Actions workflow for automated testing and deployment

## Quick Start

### Using Docker (Recommended)

1. **Start the application:**
   ```bash
   ./docker-start.sh
   ```
   This builds and starts the container at http://localhost:8080

2. **Run tests against live server:**
   ```bash
   ./run_api_tests.py
   ```

3. **Stop the application:**
   ```bash
   ./docker-start.sh stop
   ```

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

3. **Access the calculator:** http://localhost:8080

## API Endpoints

### Health Check
```bash
GET /health
```
Returns service health status and version information.

### Metrics
```bash
GET /metrics
```
Returns basic application metrics. **Note:** This is a placeholder - candidates should implement proper monitoring (Prometheus, DataDog, CloudWatch, etc.).

### Calculate Operations
```bash
POST /api/calculate
Content-Type: application/json

{
  "operation": "+",
  "a": 5,
  "b": 3
}
```

**Supported operations:** `+`, `-`, `*`, `/`, `sqrt`, `sin`, `cos`, `tan`, `log`, `ln`

### Evaluate Expressions
```bash
POST /api/evaluate
Content-Type: application/json

{
  "expression": "-5 + 10"
}
```

Supports expressions with negative numbers, decimals, and whitespace handling.

## Testing

### Live Server Testing
The application uses **HTTP integration tests** that validate the entire stack:

```bash
# Start server first
./docker-start.sh

# Run comprehensive test suite
python run_api_tests.py
```

**Features:**
- ✅ Real HTTP requests to localhost:8080
- ✅ Server connectivity validation
- ✅ 19 comprehensive integration tests
- ✅ API endpoint validation (calculate, evaluate, health, metrics)
- ✅ Error handling and edge cases
- ✅ Detailed test reporting with success breakdown

### Test Coverage
- **API Endpoints**: All calculator operations, expression evaluation, error handling
- **System Endpoints**: Health checks, metrics, main page
- **Edge Cases**: Division by zero, negative numbers, invalid operations, malformed requests

## Docker Management

The included `docker-start.sh` script provides comprehensive container management:

```bash
./docker-start.sh start    # Build and start (default)
./docker-start.sh stop     # Stop containers
./docker-start.sh logs     # View logs
./docker-start.sh status   # Check status
./docker-start.sh rebuild  # Rebuild containers
./docker-start.sh clean    # Remove everything
```

## Environment Variables

- `FLASK_ENV`: Environment (`development` or `production`)
- `PORT`: Application port (default: 8080)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FORMAT`: Log format (`json` or `console`)
- `SECRET_KEY`: Flask secret key
- `METRICS_ENABLED`: Enable/disable metrics collection

## Architecture Decisions

### Port Configuration
- **Port 8080**: Used consistently across all components (avoids macOS AirPlay conflicts)
- Docker, compose, tests, and documentation all use 8080

### Testing Strategy
- **Integration over Unit**: HTTP tests validate entire request/response cycle
- **Live Server Testing**: Tests run against actual running server
- **Real-World Validation**: Catches deployment, networking, and configuration issues

### Logging & Monitoring
- **Structured Logging**: JSON format with request correlation
- **Metrics Framework**: Basic collection ready for monitoring implementation
- **Health Checks**: Container orchestration ready

### Security
- **Non-root Container**: Runs as user `appuser` (UID 1000)
- **Multi-stage Build**: Minimal production image
- **Input Validation**: Comprehensive error handling
- **No Secrets**: Clean of hardcoded credentials

## Development Workflow

### Project Structure
```
flask-calculator-app/
├── app/
│   ├── __init__.py
│   ├── calculator.py      # Core calculation logic
│   ├── config.py         # Configuration management  
│   ├── logging_config.py # Structured logging setup
│   ├── metrics.py        # Basic metrics collection
│   └── routes.py         # API endpoints
├── static/               # Frontend assets (CSS, JS)
├── templates/            # HTML templates
├── tests/                # Integration test suite
├── docker-start.sh       # Container management script
├── run_api_tests.py      # Live server test runner
└── requirements.txt      # Python dependencies
```

### Adding Features

1. **Implement logic** in `app/calculator.py`
2. **Add API endpoint** in `app/routes.py` 
3. **Add tests** in `tests/test_routes.py`
4. **Test locally** with `python run_api_tests.py`
5. **Update documentation** as needed

### Key Design Decisions

- **Simplified Test Suite**: Single integration test file instead of redundant unit tests
- **Expression Evaluation**: Proper regex parsing for negative numbers and complex expressions
- **Container-First**: Designed for containerized deployment

