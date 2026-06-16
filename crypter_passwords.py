import mysql.connector
import bcrypt

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="magasin_informatique"
)

cursor = db.cursor(dictionary=True)

cursor.execute("SELECT id, password FROM clients")
clients = cursor.fetchall()

for client in clients:

    ancien_password = client["password"]

    hash_password = bcrypt.hashpw(
        ancien_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute(
        "UPDATE clients SET password=%s WHERE id=%s",
        (hash_password, client["id"])
    )

db.commit()

print("Hachage terminé")

cursor.close()
db.close()