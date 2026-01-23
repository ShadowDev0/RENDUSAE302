from flask import render_template, session, redirect, url_for, request
from app.machines.models import Machines
from app.logs.methodes import recuperer_logs, tri_date 

from app.logs import logs_bp

@logs_bp.route("/", methods=['GET', 'POST'])
def logs_index():
    if 'loggedin' not in session:
        return redirect(url_for('login_bp.login'))

    machines = Machines.query.all() 
    logs = []
    ids_selectionnes = [] 

    if request.method == 'POST':
        # Récupération des machines cochées
        ids_selectionnes = request.form.getlist('machine_ids')
        
        if ids_selectionnes:
            # Conversion en nombres pour la BDD
            ids_int = [int(mid) for mid in ids_selectionnes]
            machines_cibles = Machines.query.filter(Machines.id.in_(ids_int)).all()

            # Récupération
            logs_bruts = recuperer_logs(machines_cibles)
            # Tri des logs
            logs = tri_date(logs_bruts)

    return render_template(
        "logs.html", 
        machines=machines,           
        logs=logs, 
        selected_ids=ids_selectionnes
    )