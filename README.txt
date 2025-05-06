
# Projet de Prédiction de Défaut de Crédit avec LightGBM

Ce projet implémente une API de prédiction pour le défaut de crédit à l'aide du modèle de classification **LightGBM**. L'API permet de prédire si un client aura un défaut de crédit en fonction de ses données historiques.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- **Python 3.12** ou supérieur
- **pip** pour l'installation des dépendances
- **FastAPI** pour l'API web
- **LightGBM** pour le modèle de prédiction
- **pytest** pour les tests unitaires

## Installation

1. **Clonez le dépôt** sur votre machine locale.
2. **Installez les dépendances** nécessaires avec le fichier `requirements.txt` :
   - Utilisez un environnement virtuel si souhaité.
3. **Assurez-vous d'avoir les fichiers nécessaires** :
   - Le modèle **LightGBM** (`LGBMClassifier.pkl` ou `LGBMClassifier1.pkl`).
   - Le fichier de test **application_test.csv**.

## Lancer l'API

Une fois les dépendances installées, vous pouvez démarrer l'API FastAPI. L'API sera accessible à l'adresse locale par défaut : [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Endpoints de l'API

### 1. `GET /`
Retourne un message de bienvenue.

**Réponse** :
```json
{
    "message": "API de prédiction de défaut de crédit avec LightGBM"
}
```

### 2. `GET /clients`
Retourne une liste des IDs des clients disponibles dans le jeu de données de test.

**Réponse** :
```json
{
    "client_ids": [123, 456, 789, ...]
}
```

### 3. `POST /predict`
Permet de prédire le défaut de crédit pour un client donné en fonction de son `client_id`.

**Exemple de requête** :
```json
{
    "client_id": 123
}
```

**Réponse** :
```json
{
    "prediction": 1,
    "probability": 0.85
}
```

### 4. Erreur (si l'ID client est invalide)
Si l'ID client ne correspond pas à un client valide dans les données, l'API renverra une erreur 404.

**Réponse d'erreur** :
```json
{
    "detail": "Client ID non trouvé dans le jeu de test"
}
```

## Tests

Le projet inclut des tests unitaires pour vérifier le bon fonctionnement des endpoints de l'API. Les tests vérifient :
- Le message de bienvenue à l'adresse `/`.
- La récupération des IDs des clients.
- La prédiction pour un client valide et non valide.



## GitHub Actions

Le projet est configuré avec **GitHub Actions** pour automatiser les tests à chaque push ou pull request. Les workflows sont définis dans le fichier `.github/workflows/ci_api.yml`.

## Déploiement

Pour déployer cette API sur un serveur, vous pouvez utiliser des plateformes comme **Heroku**, **AWS** ou **DigitalOcean**. Consultez la documentation de la plateforme de votre choix pour déployer l'API.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez contribuer au projet, voici comment procéder :

1. Fork ce dépôt.
2. Créez une nouvelle branche (`git checkout -b feature-nouvelle-fonctionnalite`).
3. Faites vos modifications.
4. Committez vos changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`).
5. Poussez votre branche (`git push origin feature-nouvelle-fonctionnalite`).
6. Ouvrez une Pull Request.

