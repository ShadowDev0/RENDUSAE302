from flask import render_template, session, redirect, url_for, request
from app.users.models import Users
from app.users import users_bp

@users_bp.route("/", methods =['GET','POST'])
def users():
    if 'loggedin' not in session:
        return redirect(url_for('login_bp.login'))

    user = Users.query.get(session.get('id'))
    if not user or user.role_id != 3:
        return redirect(url_for('main_bp.index'))

    if request.method == 'GET':
        users = Users.query.all()
        return render_template("users.html",users=users)

    if request.method == 'POST':
        nom = request.form.get('nom')
        password = request.form.get('mot_de_passe')
        role_id = request.form.get('role_id')
        try:
            Users.create_user(nom=nom, password=password,role_id=role_id)
            return redirect ('/users')
        except Exception as error:
            print (error)


@users_bp.route("/delete/<id>")
def delete(id):
    Users.delete_user(id)
    return redirect("/users")

@users_bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    user = Users.query.get(id)

    if request.method == 'POST':
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']
        role_id = request.form['role_id']

        Users.maj_user(id, nom, mot_de_passe, role_id)
        return redirect('/users')

    return redirect("/users")