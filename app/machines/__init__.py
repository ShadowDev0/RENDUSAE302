from flask import Blueprint

machines_bp = Blueprint("machines_bp", __name__, url_prefix="/machines")


from app.machines import routes