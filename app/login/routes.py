from flask import render_template, request, redirect, url_for, session
from app.users.models import Users
from app import db
from werkzeug.security import check_password_hash

from app.login import login_bp

@login_bp.route("/", methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        account = Users.query.filter_by(nom=username).first()
        
        if account and check_password_hash(account.mot_de_passe, password):
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.nom
            session['role_id'] = account.role_id
            return redirect(url_for('main_bp.index')) 
        else:
            msg = 'Incorrect username/password!'
            
    return render_template('login.html', msg=msg)

@login_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role_id', None)
    return redirect(url_for('login_bp.login'))