import structlog
import logging
import sys
from flask import has_request_context, request
from datetime import datetime


def add_request_info(logger, method_name, event_dict):
    if has_request_context():
        event_dict["request_id"] = request.headers.get("X-Request-ID", "no-request-id")
        event_dict["method"] = request.method
        event_dict["path"] = request.path
        event_dict["remote_addr"] = request.remote_addr
    return event_dict


def setup_logging(app):
    log_level = getattr(logging, app.config["LOG_LEVEL"].upper())

    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.stdlib.add_log_level,
        add_request_info,
        timestamper,
    ]

    if app.config["LOG_FORMAT"] == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    for logger_name in ["werkzeug", "urllib3"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)

    app.logger = structlog.get_logger("flask_calculator")
