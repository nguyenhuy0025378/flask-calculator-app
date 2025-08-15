from flask import Flask
from app.config import Config
from app.logging_config import setup_logging
from app.metrics import setup_metrics


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)

    setup_logging(app)
    setup_metrics(app)

    from app.routes import main

    app.register_blueprint(main)

    return app
