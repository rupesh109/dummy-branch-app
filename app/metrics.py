from flask import Blueprint, Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

REQUEST_COUNT = Counter(
    "loan_api_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "loan_api_request_duration_seconds",
    "Request latency in seconds",
    ["endpoint"],
)

bp = Blueprint("metrics", __name__)


@bp.route("/metrics", methods=["GET"])
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
