import paramiko
from datetime import datetime

def recuperer_logs(liste_serveurs, fichier="/var/log/syslog"):
    logs = []
    
    # On initialise le client SSH
    client = paramiko.SSHClient()
    # Ajout de cette ligne car probleme de unkown host
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for serveur in liste_serveurs:
        try:
            client.connect(serveur.ip, username='app_logs', timeout=2)
            
            # Lecture du fichier
            stdin, stdout, stderr = client.exec_command(f"sudo cat {fichier}")
            contenu_brut = stdout.read().decode('utf-8', errors='ignore')
            
            for ligne in contenu_brut.splitlines():
                if not ligne.strip(): continue

                date_lisible = "Inconnu"
                msg_texte = ligne
                date_valide = datetime.min

                segments = ligne.split(maxsplit=1)
                if segments:
                    timestamp_brut = segments[0]
                    try:
                        date_valide = datetime.fromisoformat(timestamp_brut).replace(tzinfo=None)
                        date_lisible = date_valide.strftime("%Y-%m-%d %H:%M:%S")
                        msg_texte = segments[1] if len(segments) > 1 else ""
                    except ValueError:
                        try:
                            syslog_parts = ligne.split(maxsplit=3)
                            if len(syslog_parts) >= 4:
                                timestamp_brut = f"{datetime.now().year} {syslog_parts[0]} {syslog_parts[1]} {syslog_parts[2]}"
                                date_valide = datetime.strptime(timestamp_brut, "%Y %b %d %H:%M:%S")
                                date_lisible = date_valide.strftime("%Y-%m-%d %H:%M:%S")
                                msg_texte = syslog_parts[3]
                        except:
                            pass

                logs.append({
                    'machine_id': serveur.id,  
                    'machine': serveur.nom,
                    'color': getattr(serveur, 'color', '#ffffff'),
                    'timestamp': date_lisible,
                    'message': msg_texte,
                    'date_obj': date_valide
                })
            
            client.close()

        except Exception as e:
            print(f"Erreur sur {serveur.nom}: {e}")
            logs.append({
                'machine_id': serveur.id,
                'machine': serveur.nom,
                'color': '#ffcccc',
                'timestamp': 'ERREUR',
                'message': str(e),
                'date_obj': datetime.max 
            })
            continue

    return logs

def tri_date(logs):

    if not logs:
        return []

    liste_a_trier = []
    index = 0

    for log in logs:
        date_ref = datetime.min
        if log.get('timestamp') != 'ERREUR':
            d = log.get('date_obj')
            if isinstance(d, datetime):
                date_ref = d.replace(tzinfo=None)
        liste_a_trier.append((date_ref, index, log))
        index += 1
    liste_a_trier.sort(reverse=True)
    resultat = []
    for item in liste_a_trier:
        resultat.append(item[2])

    return resultat
