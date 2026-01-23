from flask import render_template, session, redirect, url_for, request
from app.users.models import Users
from app.machines.models import Machines
from app import db
from ipaddress import IPv4Address
from app.machines.scan import ping

from app.machines import machines_bp

couleurs = [
    {"hex": "#d1e7dd", "nom": "Vert"},
    {"hex": "#f8d7da", "nom": "Rouge"},
    {"hex": "#fff3cd", "nom": "Jaune"},
    {"hex": "#cff4fc", "nom": "Bleu"},
    {"hex": "#e2e3e5", "nom": "Gris"},
    {"hex": "#ffe5d0", "nom": "Orange"},
    {"hex": "#e0cffc", "nom": "Violet"},
]

@machines_bp.route("/", methods=['GET', 'POST'])
def machines():
    if 'loggedin' not in session:
        return redirect(url_for('login_bp.login'))


    user = Users.query.get(session.get('id'))
    if not user or user.role_id not in [2, 3]:
        return redirect(url_for('main_bp.index'))

    if request.method == 'GET':
        machines_list = Machines.query.all()
        server_status = []
        for m in machines_list:
            server_status.append({
                'nom': m.nom,
                'ip': m.ip,
                'online': ping(m.ip)
            })

        return render_template("machines.html", machines=machines_list, server_status=server_status, couleurs=couleurs)

    if request.method == 'POST':
        nom = request.form.get('nom')
        ip_brute = request.form.get('ip')
        color_choisie = request.form.get('color')
        
        try:
            IPv4Address(ip_brute)
            if Machines.query.filter_by(nom=nom).first():
                machines_list = Machines.query.all()
                return render_template("machines.html", machines=machines_list, couleurs=couleurs, error="Nom déjà pris")

            if not color_choisie or color_choisie not in [c['hex'] for c in couleurs]:
                color_choisie = couleurs[0]['hex'] # On prend le vert par défaut

            new_machine = Machines(nom=nom, ip=ip_brute, color=color_choisie)
            db.session.add(new_machine)
            db.session.commit()
            return redirect(url_for('machines_bp.machines'))

        except ValueError:
            machines_list = Machines.query.all()
            return render_template("machines.html", machines=machines_list, couleurs=couleurs, error="IP mal formée")
        except Exception as e:
            print(e)
            return redirect(url_for('machines_bp.machines'))

@machines_bp.route("/delete/<id>")
def delete(id):
    machine = Machines.query.get(id)
    if machine:
        db.session.delete(machine)
        db.session.commit()
    return redirect(url_for('machines_bp.machines'))

@machines_bp.route("/update/<id>", methods=['POST'])
def update(id):
    machine = Machines.query.get(id)
    if machine and request.method == 'POST':
        new_ip = request.form.get('ip')
        new_color = request.form.get('color')
        
        try:
            IPv4Address(new_ip)
            machine.ip = new_ip
            liste_codes_valides = [c['hex'] for c in couleurs]

            if new_color in liste_codes_valides:
                machine.color = new_color
            
            db.session.commit()
        except ValueError:
            pass
    return redirect(url_for('machines_bp.machines'))