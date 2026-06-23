# 💻 Magasin Informatique

Application web de gestion d'un magasin informatique développée avec **Flask**, **MySQL** et **Python**.

## 📋 Description

Ce projet permet :

- La connexion des clients
- L'inscription de nouveaux clients
- La consultation du catalogue de produits
- L'ajout de produits dans un panier
- La validation d'un paiement simulé
- L'enregistrement des commandes
- La consultation de l'historique des commandes
- L'administration des produits et des clients

---

## 🛠 Technologies utilisées

- Python 3
- Flask
- MySQL
- HTML5
- CSS3
- Git / GitHub
- bcrypt

---

## 📦 Prérequis

Avant de lancer le projet, installer :

### Python

Téléchargement :

https://www.python.org/

### MySQL Server

Téléchargement :

https://dev.mysql.com/downloads/mysql/

### MySQL Workbench

Téléchargement :

https://dev.mysql.com/downloads/workbench/

---

## 📚 Installation des bibliothèques Python

Ouvrir un terminal puis exécuter :

```bash
pip install flask
pip install mysql-connector-python
pip install bcrypt
```

Ou :

```bash
pip install flask mysql-connector-python bcrypt
```

---

## 🗄 Base de données

Créer une base de données :

```sql
CREATE DATABASE magasin_informatique;
```

Puis importer le script SQL fourni avec le projet.

Vérifier les paramètres de connexion dans le fichier `app.py` :

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="magasin_informatique"
)
```

Adapter le mot de passe MySQL si nécessaire.

---

## ▶️ Lancement de l'application

Depuis le dossier du projet :

```bash
python app.py
```

Puis ouvrir le navigateur :

```text
http://127.0.0.1:5000
```

---

## 👨‍💼 Compte administrateur

```text
Email : admin
Mot de passe : 1234
```

---

## 👤 Fonctionnalités client

- Création de compte
- Connexion
- Consultation des produits
- Ajout au panier
- Paiement simulé
- Historique des commandes

---

## 👨‍💻 Fonctionnalités administrateur

- Consultation des clients
- Consultation des produits
- Ajout de nouveaux produits
- Tableau de bord administrateur
- Visualisation des statistiques

---

## 🔒 Sécurité

Le projet utilise :

- bcrypt pour le hachage des mots de passe
- Requêtes SQL paramétrées
- Validation des formulaires

⚠️ Le paiement est une simulation pédagogique réalisée dans le cadre d'un TP. Aucune vraie donnée bancaire ne doit être utilisée.

---

## 🌐 Supervision

Le projet contient un script de supervision permettant de vérifier :

- Le service Flask (port 5000)
- Le service MySQL (port 3306)

---

## 📁 Structure du projet

```text
magasin_informatique/
│
├── app.py
├── supervision.py
├── crypter_passwords.py
├── voir_passwords.py
│
├── static/
│   ├── style.css
│   └── fond.jpg
│
└── templates/
    ├── accueil.html
    ├── login.html
    ├── inscription.html
    ├── client.html
    ├── panier.html
    ├── paiement.html
    ├── confirmation.html
    ├── historique.html
    ├── admin.html
    ├── ajouter_produit.html
    ├── commander.html
    └── produits.html
```

---

## 🎓 Projet réalisé dans le cadre d'une formation GRETA AIS

Développement d'une application Flask/MySQL avec gestion des clients, produits, commandes, panier et paiement simulé.# 💻 Magasin Informatique

Application web de gestion d'un magasin informatique développée avec **Flask**, **MySQL** et **Python**.

## 📋 Description

Ce projet permet :

- La connexion des clients
- L'inscription de nouveaux clients
- La consultation du catalogue de produits
- L'ajout de produits dans un panier
- La validation d'un paiement simulé
- L'enregistrement des commandes
- La consultation de l'historique des commandes
- L'administration des produits et des clients

---

## 🛠 Technologies utilisées

- Python 3
- Flask
- MySQL
- HTML5
- CSS3
- Git / GitHub
- bcrypt

---

## 📦 Prérequis

Avant de lancer le projet, installer :

### Python

Téléchargement :

https://www.python.org/

### MySQL Server

Téléchargement :

https://dev.mysql.com/downloads/mysql/

### MySQL Workbench

Téléchargement :

https://dev.mysql.com/downloads/workbench/

---

## 📚 Installation des bibliothèques Python

Ouvrir un terminal puis exécuter :

```bash
pip install flask
pip install mysql-connector-python
pip install bcrypt
```

Ou :

```bash
pip install flask mysql-connector-python bcrypt
```

---

## 🗄 Base de données

Créer une base de données :

```sql
CREATE DATABASE magasin_informatique;
```

Puis importer le script SQL fourni avec le projet.

Vérifier les paramètres de connexion dans le fichier `app.py` :

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="magasin_informatique"
)
```

Adapter le mot de passe MySQL si nécessaire.

---

## ▶️ Lancement de l'application

Depuis le dossier du projet :

```bash
python app.py
```

Puis ouvrir le navigateur :

```text
http://127.0.0.1:5000
```

---

## 👨‍💼 Compte administrateur

```text
Email : admin
Mot de passe : 1234
```

---

## 👤 Fonctionnalités client

- Création de compte
- Connexion
- Consultation des produits
- Ajout au panier
- Paiement simulé
- Historique des commandes

---

## 👨‍💻 Fonctionnalités administrateur

- Consultation des clients
- Consultation des produits
- Ajout de nouveaux produits
- Tableau de bord administrateur
- Visualisation des statistiques

---

## 🔒 Sécurité

Le projet utilise :

- bcrypt pour le hachage des mots de passe
- Requêtes SQL paramétrées
- Validation des formulaires

⚠️ Le paiement est une simulation pédagogique réalisée dans le cadre d'un TP. Aucune vraie donnée bancaire ne doit être utilisée.

---

## 🌐 Supervision

Le projet contient un script de supervision permettant de vérifier :

- Le service Flask (port 5000)
- Le service MySQL (port 3306)

---

## 📁 Structure du projet

```text
magasin_informatique/
│
├── app.py
├── supervision.py
├── crypter_passwords.py
├── voir_passwords.py
│
├── static/
│   ├── style.css
│   └── fond.jpg
│
└── templates/
    ├── accueil.html
    ├── login.html
    ├── inscription.html
    ├── client.html
    ├── panier.html
    ├── paiement.html
    ├── confirmation.html
    ├── historique.html
    ├── admin.html
    ├── ajouter_produit.html
    ├── commander.html
    └── produits.html
```

---

## 🎓 Projet réalisé dans le cadre d'une formation GRETA AIS

Développement d'une application Flask/MySQL avec gestion des clients, produits, commandes, panier et paiement simulé.