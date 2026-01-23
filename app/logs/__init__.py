from flask import Blueprint

logs_bp = Blueprint("logs_bp", __name__, url_prefix="/logs")

from app.logs import routes