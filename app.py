from flask import Flask, render_template, request, redirect
import mysql.connector
import bcrypt

app = Flask(__name__)

# ==========================
# CONNEXION MYSQL
# ==========================
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

        # Compte administrateur
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
# LISTE PRODUITS
# ==========================
@app.route("/produits")
def produits():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM produits
    """)

    produits = cursor.fetchall()

    cursor.close()

    return render_template(
        "produits.html",
        produits=produits
    )


# ==========================
# AJOUT PRODUIT
# ==========================
@app.route("/ajouter_produit", methods=["GET", "POST"])
def ajouter_produit():

    if request.method == "POST":

        nom = request.form["nom"]
        description = request.form["description"]
        prix = request.form["prix"]
        stock = request.form["stock"]
        image = request.form["image"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO produits
            (
                nom,
                description,
                prix,
                stock,
                image
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            nom,
            description,
            prix,
            stock,
            image
        ))

        db.commit()
        cursor.close()

        return redirect("/admin")

    return render_template("ajouter_produit.html")


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
@app.route("/inscription", methods=["GET", "POST"])
def inscription():

    if request.method == "POST":

        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        password = request.form["password"]
        adresse = request.form["adresse"]
        telephone = request.form["telephone"]

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor = db.cursor()

        cursor.execute("""
            SELECT id
            FROM clients
            WHERE email = %s
        """, (email,))

        client = cursor.fetchone()

        if client:
            cursor.close()
            return "Email déjà utilisé"

        cursor.execute("""
            INSERT INTO clients
            (
                nom,
                prenom,
                email,
                password,
                adresse,
                telephone
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            nom,
            prenom,
            email,
            password_hash,
            adresse,
            telephone
        ))

        db.commit()
        cursor.close()

        return redirect("/login")

    return render_template("inscription.html")

# ==========================
# COMMANDER
# ==========================
@app.route("/client/<int:id_client>/commander",
           methods=["GET", "POST"])
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
            (
                id_client,
                date_commande,
                total,
                statut
            )
            VALUES
            (
                %s,
                NOW(),
                %s,
                'En attente'
            )
        """, (
            id_client,
            total
        ))

        db.commit()

        id_commande = cursor.lastrowid

        cursor.execute("""
            INSERT INTO details_commandes
            (
                id_commande,
                id_produit,
                quantite,
                prix_unitaire
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
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
# DECONNEXION
# ==========================
@app.route("/logout")
def logout():
    return redirect("/")


# ==========================
# LANCEMENT
# ==========================
if __name__ == "__main__":
    app.run(debug=True)