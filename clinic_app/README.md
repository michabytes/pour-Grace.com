# Clinic Management System

Application de gestion clinique professionnelle développée en Python avec CustomTkinter et SQL Server.

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Architecture](#architecture)
- [Structure du projet](#structure-du-projet)

## ✨ Fonctionnalités

### Modules implémentés

- **Patients** : CRUD complet (Ajouter, Modifier, Supprimer, Lister, Rechercher)
- **Personnel** : Structure prête (à implémenter)
- **Chambres** : Structure prête (à implémenter)
- **Actes** : Structure prête (à implémenter)
- **Médicaments** : Structure prête (à implémenter)
- **Ordonnances** : Structure prête (à implémenter)
- **Consultations** : Structure prête (à implémenter)

### Caractéristiques techniques

- ✅ Interface 100% CustomTkinter (thème sombre professionnel)
- ✅ Zéro SQL brut - Toutes les requêtes via procédures stockées
- ✅ Architecture 3-tier (DB → Controller → UI)
- ✅ Gestion robuste des erreurs avec rollback automatique
- ✅ Notifications élégantes (succès/erreur/avertissement)
- ✅ Écran de chargement animé
- ✅ Recherche instantanée dans les tableaux
- ✅ Validation stricte des formulaires
- ✅ Typage strict Python 3.10+

## 🛠️ Prérequis

### Logiciels requis

- **Python 3.10** ou supérieur
- **SQL Server** (2016 ou supérieur recommandé)
- **ODBC Driver 17 for SQL Server** ou supérieur

### Vérification des prérequis

```bash
python --version  # Doit afficher Python 3.10+
```

## 📦 Installation

### 1. Cloner ou copier le projet

Assurez-vous que tous les fichiers sont dans le dossier `clinic_app/`.

### 2. Installer les dépendances Python

```bash
pip install customtkinter pyodbc
```

Ou avec un fichier requirements.txt :

```bash
pip install -r requirements.txt
```

### 3. Installer le driver ODBC SQL Server

#### Windows
Le driver est généralement inclus. Sinon, télécharger depuis :
https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y unixodbc-dev
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

#### macOS
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql17 mssql-tools
```

## ⚙️ Configuration

### 1. Créer la base de données SQL Server

Exécutez le script SQL pour créer les tables et procédures stockées :

```sql
-- Exemple de création des tables (à adapter selon votre schéma existant)

CREATE TABLE PATIENTS (
    IDPA INT PRIMARY KEY IDENTITY(1,1),
    PANP NVARCHAR(100) NOT NULL,
    PASX NVARCHAR(10) NOT NULL,
    PADN DATE NOT NULL,
    PALN NVARCHAR(200) NOT NULL
);

CREATE TABLE PERSONNEL (
    PEID INT PRIMARY KEY IDENTITY(1,1),
    PENP NVARCHAR(100) NOT NULL,
    STATI NVARCHAR(50) NOT NULL,
    STATM BIT NOT NULL DEFAULT 1
);

CREATE TABLE CHAMBRES (
    NUMCH NVARCHAR(20) PRIMARY KEY,
    NOLIT INT NOT NULL,
    STACH NVARCHAR(50) NOT NULL
);

CREATE TABLE ACTES (
    ACID INT PRIMARY KEY IDENTITY(1,1),
    ACDA DATETIME NOT NULL,
    ACHR NVARCHAR(200),
    ACCON NVARCHAR(MAX),
    IDPA INT FOREIGN KEY REFERENCES PATIENTS(IDPA),
    PEID INT FOREIGN KEY REFERENCES PERSONNEL(PEID)
);

CREATE TABLE MEDICAMENTS (
    IDMED INT PRIMARY KEY IDENTITY(1,1),
    NOMMED NVARCHAR(100) NOT NULL,
    DOSAGE NVARCHAR(50) NOT NULL,
    PRIX DECIMAL(10,2) NOT NULL
);

CREATE TABLE ORDONNANCE (
    IDOR INT PRIMARY KEY IDENTITY(1,1),
    ORDA DATETIME NOT NULL,
    ORMED NVARCHAR(MAX) NOT NULL,
    ORPO NVARCHAR(MAX),
    ORDU INT,
    ACID INT FOREIGN KEY REFERENCES ACTES(ACID),
    IDPA INT FOREIGN KEY REFERENCES PATIENTS(IDPA),
    PEID INT FOREIGN KEY REFERENCES PERSONNEL(PEID)
);

CREATE TABLE CONSULTATIONS (
    IDCOns INT PRIMARY KEY IDENTITY(1,1),
    DATECONS DATETIME NOT NULL,
    MOTIF NVARCHAR(200),
    DIAGNOSTIC NVARCHAR(MAX),
    IDPA INT FOREIGN KEY REFERENCES PATIENTS(IDPA),
    PEID INT FOREIGN KEY REFERENCES PERSONNEL(PEID)
);
```

### 2. Exécuter le script des procédures stockées

Ouvrez SQL Server Management Studio (SSMS) ou Azure Data Studio et exécutez le fichier `sql/procedures.sql`.

### 3. Configurer la chaîne de connexion

#### Option A : Variable d'environnement (Recommandé)

```bash
# Linux/macOS
export CLINIC_DB_CONNECTION="DRIVER={ODBC Driver 17 for SQL Server};SERVER=votre_serveur;DATABASE=ClinicDB;UID=votre_user;PWD=votre_password;"

# Windows (PowerShell)
$env:CLINIC_DB_CONNECTION="DRIVER={ODBC Driver 17 for SQL Server};SERVER=votre_serveur;DATABASE=ClinicDB;UID=votre_user;PWD=votre_password;"
```

#### Option B : Modification directe dans main.py

Éditez le fichier `clinic_app/main.py` ligne ~77 :

```python
connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=votre_serveur;DATABASE=ClinicDB;UID=votre_user;PWD=votre_password;'
```

#### Formats de chaîne de connexion

**Authentification Windows :**
```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ClinicDB;Trusted_Connection=yes;
```

**Authentification SQL Server :**
```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ClinicDB;UID=sa;PWD=VotreMotDePasse;
```

**Avec chiffrement :**
```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ClinicDB;UID=user;PWD=password;Encrypt=yes;TrustServerCertificate=yes;
```

## 🚀 Utilisation

### Lancer l'application

```bash
cd clinic_app
python main.py
```

Ou depuis la racine :

```bash
python clinic_app/main.py
```

### Navigation dans l'application

1. **Écran de chargement** : S'affiche au démarrage (1.5 secondes)
2. **Barre latérale** : Cliquez sur un module pour y accéder
3. **Tableau de données** : Affiche les éléments avec recherche instantanée
4. **Formulaire** : S'ouvre latéralement pour ajouter/modifier
5. **Notifications** : Messages contextuels pour toutes les actions

### Raccourcis clavier

- **Entrée** : Confirmer dans les dialogs
- **Échap** : Annuler/Fermer les dialogs et formulaires
- **Double-clic** : Modifier un élément dans le tableau

## 🏗️ Architecture

### Couche 1 : DatabaseManager (`database_manager.py`)

- Gestion singleton de la connexion SQL Server
- Exécution exclusive de procédures stockées
- Gestion automatique des transactions et rollbacks
- Retour structuré des résultats et erreurs

### Couche 2 : ClinicController (`clinic_controller.py`)

- Orchestration des opérations métier
- Validation des types avant envoi à la DB
- Methods typées pour chaque entité (Patients, Personnel, etc.)

### Couche 3 : UI Components (`ui_components.py`)

- **NotificationDialog** : Notifications modales élégantes
- **ConfirmationDialog** : Dialogs de confirmation
- **LoadingScreen** : Écran de chargement animé
- **StyledTreeview** : Tableau avec style sombre personnalisé

### Couche 4 : Modules (`module_*.py`)

- Interface spécifique à chaque entité
- CRUD complet avec validation
- Recherche et filtrage instantanés

## 📁 Structure du projet

```
clinic_app/
├── main.py                 # Point d'entrée principal
├── database_manager.py     # Couche d'accès aux données
├── clinic_controller.py    # Couche métier
├── ui_components.py        # Composants UI réutilisables
├── module_patients.py      # Module de gestion des patients
└── ...                     # Autres modules (à implémenter)

sql/
└── procedures.sql          # Toutes les procédures stockées

requirements.txt            # Dépendances Python
README.md                   # Ce fichier
```

## 🔒 Sécurité

- **Zéro injection SQL** : Toutes les requêtes sont paramétrées via procédures stockées
- **Validation des entrées** : Tous les champs sont validés avant envoi
- **Gestion des erreurs** : Try/catch avec rollback automatique
- **Données sensibles** : La chaîne de connexion peut être externalisée via variables d'environnement

## 🐛 Dépannage

### Erreur de connexion à la base de données

1. Vérifiez que SQL Server est en cours d'exécution
2. Testez la connectivité avec `telnet serveur 1433`
3. Vérifiez les identifiants dans la chaîne de connexion
4. Assurez-vous que le driver ODBC est installé

### L'application ne démarre pas

1. Vérifiez la version Python : `python --version`
2. Réinstallez les dépendances : `pip install -r requirements.txt --force-reinstall`
3. Vérifiez les logs console pour les erreurs d'import

### Erreur "Module not found"

Assurez-vous d'exécuter depuis le bon répertoire ou ajoutez le chemin :

```bash
export PYTHONPATH="${PYTHONPATH}:/chemin/vers/clinic_app"
```

## 📝 Notes de développement

### Ajouter un nouveau module

1. Créez les procédures stockées dans `sql/procedures.sql`
2. Ajoutez les méthodes dans `clinic_controller.py`
3. Créez le fichier `module_nom.py` sur le modèle de `module_patients.py`
4. Ajoutez le bouton de navigation dans `main.py`

### Bonnes pratiques respectées

- ✅ Typage strict avec type hints
- ✅ Docstrings complètes
- ✅ Respect PEP8
- ✅ Noms de variables explicites
- ✅ Gestion centralisée des erreurs
- ✅ Code DRY (Don't Repeat Yourself)
- ✅ Séparation des responsabilités

## 📄 License

Ce projet est fourni à titre éducatif et professionnel.

## 👥 Support

Pour toute question ou problème, consultez la documentation technique ou contactez l'équipe de développement.

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2024  
**Développé avec** ❤️ en Python & CustomTkinter
