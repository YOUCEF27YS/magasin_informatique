import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="magasin_informatique"
)

cursor = db.cursor()

cursor.execute(
    "SELECT id, email, password FROM clients"
)

for ligne in cursor.fetchall():
    print(ligne)

db.close()