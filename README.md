# GeoMarketing AI Agents

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Un projet open source d'agents IA pour le géomarketing, combinant DeepSeek R1 avec des outils d'analyse géospatiale pour optimiser les décisions géographiques.

## 🌟 Fonctionnalités

Le projet propose deux agents IA spécialisés :

### 🏪 Agent d'optimisation d'emplacement commercial

Trouvez le meilleur emplacement pour votre commerce en analysant :
- Données démographiques et socio-économiques
- Flux de circulation et accessibilité
- Concurrence et points d'intérêt
- Visibilité et potentiel commercial

Idéal pour : pharmacies, commerces de détail, restaurants, services...

### 🌱 Agent d'analyse de la qualité des sols

Évaluez la compatibilité de vos terrains avec différentes cultures en analysant :
- Propriétés pédologiques (texture, pH, matière organique)
- Capacité de drainage et rétention d'eau
- Zonage des parcelles
- Recommandations agronomiques

Idéal pour : agriculteurs, agronomes, projets de plantation...

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/username/geomarketing-ai-agents.git
cd geomarketing-ai-agents

# Créer et activer un environnement virtuel
# Sur Linux/macOS
python -m venv geo
source geo/bin/activate

# Sur Windows
conda create -n geo_env python=3.9
conda activate geo_env
conda install -c conda-forge geopandas osmnx folium

# Installer les dépendances
cd C:\Users\daniel.razakamanana\Downloads\geomarketing-ai-agents
pip install -r requirements.txt

# Lancer l'application
python src/main.py
```

L'application sera accessible à l'adresse [http://localhost:5000](http://localhost:5000).

## 📊 Utilisation

### Analyse d'emplacement commercial

1. Accédez à la page "Emplacement Commercial" depuis le menu principal
2. Entrez la localisation que vous souhaitez analyser (ville, quartier, adresse)
3. Sélectionnez le type de commerce (pharmacie, boulangerie, etc.)
4. Ajustez les paramètres selon vos besoins (rayon d'analyse, facteurs d'importance)
5. Cliquez sur "Analyser" pour lancer l'analyse
6. Consultez les résultats sous forme de scores, cartes et recommandations

### Analyse de la qualité des sols

1. Accédez à la page "Qualité des Sols" depuis le menu principal
2. Entrez la localisation de votre parcelle (ville, région, coordonnées)
3. Sélectionnez le type de culture que vous souhaitez évaluer (stevia, blé, etc.)
4. Ajustez les paramètres selon vos besoins (profondeur d'analyse, facteurs d'importance)
5. Cliquez sur "Analyser" pour lancer l'analyse
6. Consultez les résultats sous forme de scores, cartes de zones et recommandations agronomiques

## 🧠 Technologies utilisées

### Intelligence Artificielle
- **DeepSeek R1** : Modèle d'IA avancé pour le raisonnement et l'analyse de données géospatiales

### Backend
- **Flask** : Framework web Python
- **GeoPandas** : Manipulation de données géospatiales
- **OSMnx** : Accès aux données OpenStreetMap
- **Folium** : Génération de cartes interactives
- **Matplotlib** : Visualisation de données

### Frontend
- **Bootstrap** : Framework CSS
- **JavaScript** : Interactivité côté client
- **Leaflet** : Bibliothèque de cartographie

### Sources de données
- **OpenStreetMap** : Données géographiques (réseau routier, bâtiments, POI)
- **INSEE** : Données démographiques et socio-économiques
- **INRAE** : Référentiels Régionaux Pédologiques
- **FAO** : Harmonized World Soil Database

## 📁 Structure du projet

```
geomarketing-ai-agents/
├── src/
│   ├── models/       # Modèles de données
│   ├── routes/       # Routes API
│   │   ├── commercial_routes.py
│   │   └── soil_routes.py
│   ├── services/     # Services métier
│   │   ├── commercial_location_service.py
│   │   └── soil_quality_service.py
│   ├── static/       # Fichiers statiques
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   └── visualizations/
│   ├── templates/    # Templates HTML
│   │   ├── index.html
│   │   ├── commercial.html
│   │   ├── soil.html
│   │   ├── docs.html
│   │   ├── 404.html
│   │   └── 500.html
│   ├── utils/        # Utilitaires
│   │   └── deepseek_client.py
│   └── main.py       # Point d'entrée
├── venv/             # Environnement virtuel
├── requirements.txt  # Dépendances
├── LICENSE           # Licence du projet
└── README.md         # Documentation
```

## 🔌 API

Le projet expose des API REST pour l'intégration avec d'autres applications :

### Analyse d'emplacement commercial

```http
POST /api/commercial/analyze
Content-Type: application/json

{
    "location": "Paris, France",
    "business_type": "pharmacie",
    "parameters": {
        "radius": 500,
        "importance_factors": {
            "population": 0.4,
            "competition": 0.3,
            "accessibility": 0.3
        }
    }
}
```

### Analyse de la qualité des sols

```http
POST /api/soil/analyze
Content-Type: application/json

{
    "location": "Toulouse, France",
    "crop_type": "stevia",
    "parameters": {
        "depth": 30,
        "importance_factors": {
            "ph": 0.3,
            "drainage": 0.3,
            "texture": 0.2,
            "organic_matter": 0.2
        }
    }
}
```

## 🛠️ Extension du projet

Le projet est conçu pour être facilement extensible :

### Intégration de nouvelles sources de données

Pour ajouter une nouvelle source de données, créez un nouveau module dans `src/utils` qui implémente les méthodes d'accès à cette source, puis intégrez-le dans les services existants.

### Ajout de nouveaux types d'analyses

Pour ajouter un nouveau type d'analyse, créez un nouveau service dans `src/services`, une nouvelle route dans `src/routes`, et les templates correspondants dans `src/templates`.

### Intégration avec d'autres modèles d'IA

Le client DeepSeek R1 est conçu pour être facilement remplaçable. Modifiez `src/utils/deepseek_client.py` pour intégrer un autre modèle d'IA, en conservant la même interface.

## 📝 Notes importantes

- Dans la version actuelle, les résultats sont basés sur des données simulées pour démonstration
- Pour une utilisation en production, il est recommandé d'intégrer des sources de données réelles et de calibrer les modèles d'analyse

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à soumettre des pull requests ou à ouvrir des issues pour améliorer le projet.

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à nous contacter.

---

Développé avec ❤️ par l'équipe GeoMarketing AI
