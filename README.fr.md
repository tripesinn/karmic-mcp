# Serveur Karmic Lite MCP (Documentation Français)

## 🚀 Vue d'ensemble
Le Serveur Karmic Lite MCP est un microservice FastAPI haute efficacité conçu pour fournir des données astrologiques et doctrinales Karmic Lite via le Protocole de Contexte Modèle (MCP). Il fournit des points de terminaison de base pour les calculs de transits planétaires et des lectures doctrinales spécialisées basées sur les données du thème natal.

## 🛠️ Prérequis
*   Python 3.12+ (Recommandé pour une compatibilité optimale des dépendances)
*   `uvicorn` et `fastapi` (Dépendances listées dans `requirements.txt`)
*   L'implémentation de la logique principale (`karmic_lite.py`) doit être disponible dans le répertoire racine du projet.

## ⚙️ Configuration Locale et Installation

1.  **Cloner le référentiel** (si applicable).
2.  **Installer les dépendances:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Lancer le serveur:**
    ```bash
    python server.py
    ```
    *Le serveur démarrera sur `http://0.0.0.0:8000`.*

## 🧪 Tests Locaux et Validation

Utilisez les commandes suivantes pour valider les points de terminaison de l'API et confirmer la compatibilité du schéma MCP.

### 1. Vérification de la Santé
Vérifiez si le service est opérationnel :
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/health
# Sortie Attendue: 200
```

### 2. Schéma de Découverte MCP
Vérifiez les métadonnées du service requises par la Galerie Edge:
```bash
curl -s http://localhost:8000/mcp/discovery | json_pp
# Sortie Attendue: Une structure JSON détaillant les points de terminaison disponibles.
```

### 3. Test des Transits Planétaires (Exemple: Données Natales de Jero)
Utilisez une date de naissance valide (DOB) pour tester le point de terminaison des transits. (DOB Exemple: `2026-06-20`).
```bash
curl -X GET "http://localhost:8000/transits/today?dob=2026-06-20" | json_pp
# Sortie Attendue: Un objet JSON correspondant au schéma TransitResponse.
# Structure Exemple: {"date": "2026-06-20", "planet_positions": {"sun": "Cancer", "moon": "Gemini"}}
```

### 4. Test de la Lecture Doctrinale
Testez le point de terminaison de lecture doctrinale avec DOB et heure de naissance précise.
```bash
curl -X POST "http://localhost:8000/doctrine/reading?dob=2026-06-20&birth_time=14:30" \
  -H "Content-Type: application/json" -d '{}' | json_pp
# Sortie Attendue: Un objet JSON correspondant au schéma DoctrineResponse.
# Structure Exemple: {"reading": "A doctrine reading for 2026-06-20 at 14:30. (Mocked content)", "input_details": {...}}
```

## 🌐 Inscription Edge Gallery
Une fois les tests locaux terminés, le service est prêt pour l'enregistrement auprès de la Galerie Edge. Le point de terminaison `/mcp/discovery` fournit toutes les informations de schéma nécessaires pour la configuration automatique. Suivez la documentation officielle de la Galerie Edge pour le processus d'inscription.