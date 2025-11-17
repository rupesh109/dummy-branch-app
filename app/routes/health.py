from flask import Blueprint, jsonify
from app.db import SessionContext
from sqlalchemy import text  

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health():
    try:
        
        with SessionContext() as session:
            
            session.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "db": "up"
        }), 200
    except Exception as exc:
        return jsonify({
            "status": "error",
            "db": "down",
            "details": str(exc),
        }), 500
