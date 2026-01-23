from flask import Blueprint

login_bp = Blueprint("login_bp", __name__, url_prefix="/login", template_folder="templates")

from app.login import routes