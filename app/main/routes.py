from flask import render_template, session, redirect, url_for

from app.main import main_bp

@main_bp.route("/")
def index():
    if 'loggedin' not in session:
        return redirect(url_for('login_bp.login'))
    return render_template("index.html")