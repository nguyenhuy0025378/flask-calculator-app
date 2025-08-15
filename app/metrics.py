import time
from flask import request
from functools import wraps


# Basic metrics tracking - candidates should implement their own monitoring solution
class MetricsCollector:
    def __init__(self):
        self.request_count = {}
        self.request_duration = []
        self.start_time = time.time()

    def track_request(self, method, endpoint, status, duration):
        """Track basic request metrics"""
        key = f"{method}:{endpoint}:{status}"
        self.request_count[key] = self.request_count.get(key, 0) + 1
        self.request_duration.append(
            {
                "method": method,
                "endpoint": endpoint,
                "duration": duration,
                "timestamp": time.time(),
            }
        )

    def get_stats(self):
        """Get basic statistics"""
        uptime = time.time() - self.start_time
        total_requests = sum(self.request_count.values())
        avg_duration = (
            sum(d["duration"] for d in self.request_duration)
            / len(self.request_duration)
            if self.request_duration
            else 0
        )

        return {
            "uptime_seconds": uptime,
            "total_requests": total_requests,
            "average_duration": avg_duration,
            "request_counts": self.request_count,
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()


def track_metrics(f):
    """Decorator to track metrics for routes"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()

        try:
            response = f(*args, **kwargs)
            status = response[1] if isinstance(response, tuple) else 200
        except Exception as e:
            status = 500
            raise
        finally:
            duration = time.time() - start_time
            metrics_collector.track_request(
                method=request.method,
                endpoint=request.endpoint or "unknown",
                status=status,
                duration=duration,
            )

        return response

    return decorated_function


def setup_metrics(app):
    """Setup basic metrics collection"""
    if not app.config.get("METRICS_ENABLED", True):
        return

    # Basic metrics endpoint - candidates should implement proper monitoring
    @app.route("/metrics")
    def metrics():
        """
        Basic metrics endpoint placeholder.
        Candidates should implement proper monitoring (Prometheus, DataDog, etc.)
        """
        stats = metrics_collector.get_stats()
        return {
            "status": "ok",
            "metrics": stats,
            "note": "Implement proper monitoring solution (Prometheus, DataDog, CloudWatch, etc.)",
        }

    @app.before_request
    def before_request():
        request._start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time
            metrics_collector.track_request(
                method=request.method,
                endpoint=request.endpoint or "unknown",
                status=response.status_code,
                duration=duration,
            )

        return response
