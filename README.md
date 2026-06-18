# 🏠 Ymmo — Plateforme Immobilière

Ymmo est une plateforme web de gestion de biens immobiliers développée dans le cadre du projet UF B2 INFRA & DEV — Ynov Informatique.

## 📋 Fonctionnalités

- 🔍 Recherche et filtrage de biens immobiliers
- 📄 Fiches détaillées avec photos, prix, surface
- 👤 Système d'inscription et connexion (client / agent / admin)
- ❤️ Gestion des favoris
- 📩 Messagerie client → agence
- ➕ Publication et suppression d'annonces (agents)
- 📊 Tableau de bord agent avec statistiques
- 📈 Page d'analyse du marché immobilier (graphiques)

## 🛠️ Stack technique

| Technologie | Usage |
|------------|-------|
| Python / Flask | Backend |
| SQLite / SQLAlchemy | Base de données |
| Jinja2 | Templates HTML |
| Bootstrap 5 | Interface responsive |
| Chart.js | Graphiques et analytics |

## 🚀 Installation

```bash
# 1. Cloner le projet
git clone https://github.com/YarkinOner/ymmo.git
cd ymmo

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Initialiser la base de données avec des données de test
python seed.py

# 4. Lancer le serveur
python app.py
```

Ouvrir http://127.0.0.1:5000 dans le navigateur.

## 👤 Compte de test

| Email | Mot de passe | Rôle |
|-------|-------------|------|
| admin@ymmo.fr | admin123 | Admin |

## 📁 Structure du projet
ymmo/

├── app.py              # Point d'entrée Flask

├── models.py           # Modèles SQLAlchemy

├── routes/

│   ├── auth.py         # Authentification

│   ├── listings.py     # Annonces

│   ├── dashboard.py    # Tableau de bord

│   └── analytics.py    # Analyse du marché

├── templates/          # Pages HTML (Jinja2)

├── static/css/         # Styles CSS

├── seed.py             # Données de test

├── requirements.txt    # Dépendances Python

└── INFRA.md            # Documentation infrastructure

## 👥 Équipe

Projet réalisé dans le cadre du Bachelor 2 Informatique — Ynov Campus.

Yarkin Oner

