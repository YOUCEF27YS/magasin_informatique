import socket
from datetime import datetime


def verifier_port(port):

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    resultat = s.connect_ex(
        ("127.0.0.1", port)
    )

    s.close()

    return resultat == 0


flask_actif = verifier_port(5000)
mysql_actif = verifier_port(3306)

date_test = datetime.now()

rapport = f"""
Date : {date_test}

Flask (5000) :
{'ACTIF' if flask_actif else 'INACTIF'}

MySQL (3306) :
{'ACTIF' if mysql_actif else 'INACTIF'}

Statut général :
{'OK' if flask_actif and mysql_actif else 'PROBLEME'}
"""

print(rapport)

with open(
    "rapport.txt",
    "w",
    encoding="utf-8"
) as fichier:

    fichier.write(rapport)

print("Rapport enregistré dans rapport.txt")