# L'Observatoire Météo

Projet fil rouge Meteo. L'application suit une donnée météo de bout en bout :

```
API Open-Meteo  →  validation Pydantic  →  stockage SQLite (SQLAlchemy)  →  API FastAPI documentée
```

Elle se compose de deux programmes indépendants :

- **la collecte** (`main.py`) interroge Open-Meteo pour une liste de villes, valide les réponses et enregistre villes et relevés dans la base ;
- **l'API** (`api.py`) expose le contenu de la base en lecture, avec une documentation Swagger générée automatiquement.

## Installation

Prérequis : Python 3.10 ou plus récent.

Depuis le dossier `api_meteo/` :

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Copier ensuite `.env.example` en `.env`. Ce fichier indique l'emplacement de la base de données :

```
DATABASE_URL=sqlite:///./database/ma_bdd.db
```


## Utilisation

### 1. Collecter les données

```bash
python main.py
```

Au premier lancement, le script crée les tables. Ensuite, pour chaque ville de la liste définie dans `main.py` :

1. il récupère ses coordonnées auprès de l'API de géocodage d'Open-Meteo ;
2. il enregistre la ville si elle n'est pas déjà en base ;
3. il récupère la météo actuelle et l'enregistre si ce relevé n'est pas déjà en base.

Il affiche enfin les statistiques de température par ville.


### 2. Lancer l'API

```bash
uvicorn api:app --reload
```

- API : <http://127.0.0.1:8000>
- Documentation interactive (Swagger) : <http://127.0.0.1:8000/docs>

## Routes

| Méthode | Route | Description | Codes de retour |
|---|---|---|---|
| GET | `/` | Route de test | 200 |
| GET | `/villes` | Liste des villes enregistrées | 200 |
| GET | `/meteo/{ville}` | Relevés d'une ville, du plus ancien au plus récent | 200 ; 404 si la ville est inconnue ; 404 si elle n'a aucun relevé |
| GET | `/stats` | Par ville : nombre de relevés, température minimale, maximale et moyenne | 200 |

Le nom de la ville dans `/meteo/{ville}` ne tient pas compte des majuscules : `/meteo/paris` et `/meteo/Paris` donnent le même résultat.

**Les heures des relevés sont en GMT.** C'est le fuseau qu'utilise Open-Meteo.

## Structure du projet

```
api_meteo/
├── main.py                  Script de collecte
├── api.py                   Application FastAPI (routes)
├── core/
│   ├── config.py            Lecture de la configuration (.env)
│   ├── database.py          Moteur SQLAlchemy, sessions, get_db pour FastAPI
│   └── utils.py             Fonctions d'affichage console
├── models/                  Modèles ORM (tables de la base)
│   ├── ville.py             Table villes
│   └── releve.py            Table releves (clé étrangère vers villes)
├── schemas/                 Schémas Pydantic
│   ├── weather_response.py  Réponse complète de l'API météo
│   ├── ville_schema.py      Ville reçue du géocodage / ville renvoyée par l'API
│   ├── releve_schema.py     Relevé reçu d'Open-Meteo / relevé renvoyé par l'API
│   └── stats_schema.py      Statistiques renvoyées par l'API
├── services/                Logique métier et accès aux données
│   ├── ville_service.py     Géocodage, recherche et insertion des villes
│   ├── releve_service.py    Appel météo, recherche et insertion des relevés
│   └── stats_service.py     Calcul et affichage des statistiques
└── database/                Base SQLite (fichier créé au premier lancement, non versionné)
```

Les schémas Pydantic sont séparés en deux familles :

- **schémas d'entrée** (`VilleSchema`, `ReleveSchema`, `WeatherResponseModel`) : ils valident les données reçues d'Open-Meteo et traduisent leurs noms (`name` → `nom`, `windspeed` → `vitesse_vent`, `time` → `date_heure`) ;
- **schémas de sortie** (`VilleReponse`, `ReleveReponse`, `StatVille`) : ils décrivent ce que l'API renvoie à ses clients et apparaissent dans Swagger.

## Base de données

| Table | Colonnes |
|---|---|
| `villes` | `id`, `nom` (unique), `latitude`, `longitude` |
| `releves` | `id`, `temperature`, `vitesse_vent`, `date_heure`, `ville_id` (clé étrangère vers `villes.id`) |

Les doublons sont évités par le code avant chaque insertion :

- une ville n'est pas réinsérée si une ville du même nom existe déjà ;
- un relevé n'est pas réinséré s'il existe déjà un relevé pour la même ville et la même `date_heure`.

## Limites connues

- La recherche d'une ville sans tenir compte des majuscules repose sur la fonction `lower()` de SQLite, qui ne traite que les lettres sans accent. Une ville dont le nom commence par une majuscule accentuée (« Évry ») ne sera pas trouvée si on la saisit en minuscules.
- Le géocodage retient le premier résultat proposé par Open-Meteo. Pour un nom porté par plusieurs villes, ce n'est pas forcément celle attendue.
- Les heures sont stockées sans fuseau horaire (SQLite ne les gère pas). Elles sont en GMT.
- La liste des villes collectées est écrite directement dans `main.py`.

## Technologies

| Rôle | Outil |
|---|---|
| Source des données | API Open-Meteo (prévisions et géocodage) |
| Appels HTTP | requests |
| Validation | Pydantic |
| Base de données | SQLite, via l'ORM SQLAlchemy |
| API | FastAPI, servie par Uvicorn |
| Configuration | python-dotenv |
