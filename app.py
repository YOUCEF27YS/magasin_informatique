from flask import Flask, render_template, request, redirect
import mysql.connector
import bcrypt

app = Flask(__name__)

# Connexion MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="magasin_informatique"
)

# ==========================
# ACCUEIL
# ==========================
@app.route("/")
def accueil():
    return render_template("accueil.html")


# ==========================
# LOGIN
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        # ADMIN
        if email == "admin" and password == "1234":
            return redirect("/admin")

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM clients WHERE email=%s",
            (email,)
        )

        client = cursor.fetchone()

        cursor.close()

        if client:

            try:
                if bcrypt.checkpw(
                    password.encode("utf-8"),
                    client["password"].encode("utf-8")
                ):
                    return redirect(f"/client/{client['id']}")
            except:
                pass

        return "Erreur login"

    return render_template("login.html")


# ==========================
# ADMIN
# ==========================
@app.route("/admin")
def admin():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    cursor.execute("""
        SELECT id, nom, prenom, email
        FROM clients
    """)
    clients = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin.html",
        produits=produits,
        clients=clients
    )


# ==========================
# PAGE CLIENT
# ==========================
@app.route("/client/<int:id_client>")
def client(id_client):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT produits.nom,
               produits.prix,
               details_commandes.quantite

        FROM details_commandes

        JOIN produits
        ON produits.id = details_commandes.id_produit

        WHERE details_commandes.id_commande IN (
            SELECT id
            FROM commandes
            WHERE id_client = %s
        )
    """, (id_client,))

    produits = cursor.fetchall()

    cursor.close()

    return render_template(
        "client.html",
        produits=produits,
        id_client=id_client
    )


# ==========================
# COMMANDER
# ==========================
@app.route("/client/<int:id_client>/commander", methods=["GET", "POST"])
def commander(id_client):

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    if request.method == "POST":

        id_produit = int(request.form["id_produit"])
        quantite = int(request.form["quantite"])

        cursor.execute(
            "SELECT * FROM produits WHERE id=%s",
            (id_produit,)
        )

        produit = cursor.fetchone()

        if not produit:
            cursor.close()
            return "Produit introuvable"

        if produit["stock"] < quantite:
            cursor.close()
            return "Stock insuffisant"

        total = float(produit["prix"]) * quantite

        cursor.execute("""
            INSERT INTO commandes
            (id_client, date_commande, total, statut)

            VALUES
            (%s, NOW(), %s, 'En attente')
        """, (id_client, total))

        db.commit()

        id_commande = cursor.lastrowid

        cursor.execute("""
            INSERT INTO details_commandes
            (id_commande, id_produit, quantite, prix_unitaire)

            VALUES
            (%s, %s, %s, %s)
        """, (
            id_commande,
            id_produit,
            quantite,
            produit["prix"]
        ))

        cursor.execute("""
            UPDATE produits
            SET stock = stock - %s
            WHERE id = %s
        """, (
            quantite,
            id_produit
        ))

        db.commit()

        cursor.close()

        return redirect(f"/client/{id_client}")

    cursor.close()

    return render_template(
        "commander.html",
        produits=produits,
        id_client=id_client
    )


# ==========================
# LANCEMENT
# ==========================
if __name__ == "__main__":
    app.run(debug=True)