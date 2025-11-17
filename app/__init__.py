import logging
import sys
import uuid
import time

from flask import Flask, g, request
from pythonjsonlogger import jsonlogger

from .config import Config
from .metrics import bp as metrics_bp, REQUEST_COUNT, REQUEST_LATENCY


def configure_logging(app: Flask) -> None:
    """Configure JSON structured logging for the app."""
    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s "
        "%(request_id)s %(path)s %(method)s %(status_code)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = []          
    root_logger.addHandler(handler)

    log_level = app.config.get("LOG_LEVEL", "INFO").upper()
    root_logger.setLevel(log_level)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    configure_logging(app)

    
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)                 # /health
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")
    app.register_blueprint(metrics_bp)                # /metrics

    @app.before_request
    def start_request():
        """Attach request id and start time for metrics and logging."""
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()

    @app.after_request
    def log_and_measure(response):
        """Log each request and record Prometheus metrics."""
        endpoint = request.endpoint or "unknown"
        duration = time.time() - g.get("start_time", time.time())

        if request.path != "/metrics":
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=response.status_code,
            ).inc()

        extra = {
            "request_id": getattr(g, "request_id", None),
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
        }
        app.logger.info("request", extra=extra)

        if getattr(g, "request_id", None):
            response.headers["X-Request-ID"] = g.request_id

        return response

    return app
