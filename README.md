# CRM Django

Ce projet est un CRM (Customer Relationship Management) développé en Django. Il permet de stocker et de manipuler de manière sécurisée les informations des clients, ainsi que les contrats et les événements organisés. Le logiciel fonctionne en ligne de commande, utilise SQLite comme base de données et Sentry pour la gestion des erreurs.

## Fonctionnalités

- Gestion des clients : Ajout, modification, lecture et suppression des informations des clients.
- Gestion des contrats : Ajout, modification, lecture et suppression des contrats associés aux clients.
- Gestion des événements : Ajout, modification, lecture et suppression des événements pour les clients.
- Journalisation des actions importantes.
- Intégration de Sentry pour la gestion des erreurs et le suivi des performances.

## Prérequis

- Python 3.8 ou supérieur
- Django 3.2 ou supérieur
- pip (Python package installer)
- Sentry (compte et DSN)

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/KassimBouzoubaa/epic_events.git
    cd epicevents
    ```

2. Créez un environnement virtuel et activez-le :

    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
    ```

3. Installez les dépendances requises :

    ```bash
    pip install -r requirements.txt
    ```

4. Configurez les variables d'environnement. Créez un fichier `.env` à la racine du projet et ajoutez-y vos paramètres Sentry :

    ```env
    SENTRY_DSN=https://votre-dsn-sentry
    ```

5. Initialisez la base de données avec les données de départ :

    ```bash
    python manage.py migrate
    python manage.py loaddata initial_data.json
    ```

## Utilisation

Le logiciel fonctionne principalement via la ligne de commande. Voici quelques commandes utiles :

- **Créer un utilisateur :**

    ```bash
    python manage.py gestion_commands create_collaborateur <nom> <prenom> <username> <email> <role> <password>
    ```

- **Modifier un utilisateur :**

    ```bash
    python manage.py gestion_commands update_collaborateur <user_id> <nom> <prenom> <email> <role>
    ```

- **Créer un contrat :**

    ```bash
    python manage.py gestion_commands create_contract <montant_total> <client_id> <commercial_id>
    ```

- **Démarrer le serveur de développement :**

    ```bash
    python manage.py runserver
    ```

## Journalisation

Les actions importantes, comme la création ou la modification de collaborateurs et de contrats, sont journalisées pour un suivi détaillé. Les journaux peuvent être consultés dans la console ou envoyés à Sentry pour une analyse plus approfondie.

## Gestion des erreurs

Sentry est intégré pour la gestion des erreurs et le suivi des performances. Assurez-vous que la variable d'environnement `SENTRY_DSN` est correctement configurée pour capturer et envoyer les erreurs à Sentry.