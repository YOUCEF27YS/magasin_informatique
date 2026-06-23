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

    # Produits
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    # Clients
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()

    # Nombre commandes
    cursor.execute("SELECT COUNT(*) AS total FROM commandes")
    nb_commandes = cursor.fetchone()["total"]

    # Chiffre d'affaires
    cursor.execute("""
        SELECT SUM(total) AS ca
        FROM commandes
        WHERE statut='Payée'
    """)

    resultat = cursor.fetchone()

    chiffre_affaires = resultat["ca"] if resultat["ca"] else 0

    cursor.close()

    return render_template(
        "admin.html",
        produits=produits,
        clients=clients,
        nb_commandes=nb_commandes,
        chiffre_affaires=chiffre_affaires
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

    cursor.execute(
        "SELECT * FROM clients WHERE id=%s",
        (id_client,)
    )

    client = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM produits"
    )

    produits = cursor.fetchall()

    cursor.close()

    return render_template(
        "client.html",
        client=client,
        produits=produits,
        id_client=id_client
    )

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
@app.route("/historique/<int:id_client>")
def historique(id_client):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            commandes.id,
            commandes.date_commande,
            commandes.total,
            commandes.statut
        FROM commandes
        WHERE id_client=%s
        ORDER BY date_commande DESC
    """, (id_client,))

    commandes = cursor.fetchall()

    cursor.close()

    return render_template(
        "historique.html",
        commandes=commandes,
        id_client=id_client
    )

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
@app.route("/ajouter_panier/<int:id_client>/<int:id_produit>")
def ajouter_panier(id_client, id_produit):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT stock FROM produits WHERE id=%s",
        (id_produit,)
    )

    produit = cursor.fetchone()

    if not produit:
        return "Produit introuvable"

    cursor.execute("""
        SELECT *
        FROM panier
        WHERE id_client=%s
        AND id_produit=%s
    """, (id_client, id_produit))

    article = cursor.fetchone()

    if article:

        cursor.execute("""
            UPDATE panier
            SET quantite = quantite + 1
            WHERE id_client=%s
            AND id_produit=%s
        """, (id_client, id_produit))

    else:

        cursor.execute("""
            INSERT INTO panier
            (id_client,id_produit,quantite)
            VALUES(%s,%s,%s)
        """, (id_client,id_produit,1))

    db.commit()

    return redirect(f"/panier/{id_client}")
@app.route("/panier/<int:id_client>")
def panier(id_client):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
        panier.id,
        produits.nom,
        produits.prix,
        panier.quantite,
        produits.prix * panier.quantite AS total

        FROM panier

        JOIN produits
        ON produits.id = panier.id_produit

        WHERE panier.id_client=%s
    """, (id_client,))

    produits = cursor.fetchall()

    total_panier = sum(
        produit["total"]
        for produit in produits
    )

    return render_template(
        "panier.html",
        produits=produits,
        total_panier=total_panier,
        id_client=id_client
    )
@app.route("/paiement/<int:id_client>", methods=["GET", "POST"])
def paiement(id_client):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            panier.id_produit,
            panier.quantite,
            produits.prix,
            produits.prix * panier.quantite AS total

        FROM panier

        JOIN produits
        ON produits.id = panier.id_produit

        WHERE panier.id_client=%s
    """, (id_client,))

    produits = cursor.fetchall()

    total_panier = sum(
        produit["total"]
        for produit in produits
    )

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO commandes
            (id_client, date_commande, total, statut)
            VALUES
            (%s, NOW(), %s, 'Payée')
        """, (
            id_client,
            total_panier
        ))

        db.commit()

        id_commande = cursor.lastrowid

        for produit in produits:

            cursor.execute("""
                INSERT INTO details_commandes
                (id_commande, id_produit, quantite, prix_unitaire)
                VALUES
                (%s,%s,%s,%s)
            """, (
                id_commande,
                produit["id_produit"],
                produit["quantite"],
                produit["prix"]
            ))

        cursor.execute("""
            DELETE FROM panier
            WHERE id_client=%s
        """, (id_client,))

        db.commit()

        cursor.close()

        return render_template(
            "confirmation.html",
            id_client=id_client,
            id_commande=id_commande,
            total_panier=total_panier
        )

    cursor.close()

    return render_template(
        "paiement.html",
        total_panier=total_panier
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

  