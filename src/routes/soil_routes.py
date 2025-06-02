"""
Routes pour l'API d'analyse de la qualité des sols.
"""
from flask import Blueprint, request, jsonify, render_template
from src.services.soil_quality_service import SoilQualityService

# Création du blueprint
soil_bp = Blueprint('soil', __name__, url_prefix='/api/soil')

# Initialisation du service
soil_service = SoilQualityService(use_mock=True)

@soil_bp.route('/analyze', methods=['POST'])
def analyze_soil():
    """
    Endpoint pour analyser la qualité des sols.
    
    Exemple de requête:
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
    """
    data = request.json
    
    if not data or 'location' not in data:
        return jsonify({"error": "La localisation est requise"}), 400
    
    location = data.get('location')
    crop_type = data.get('crop_type', 'stevia')
    parameters = data.get('parameters', {})
    
    # Appel au service d'analyse
    results = soil_service.analyze_soil(location, crop_type, parameters)
    
    # Transformation des chemins de fichiers en URLs relatives
    if 'visualizations' in results:
        for key, path in results['visualizations'].items():
            if path.startswith('src/static/'):
                results['visualizations'][key] = '/' + path.replace('src/static/', 'static/')
    
    return jsonify(results)

@soil_bp.route('/examples', methods=['GET'])
def get_examples():
    """Renvoie des exemples de paramètres pour l'analyse de la qualité des sols."""
    examples = [
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
        },
        {
            "location": "Bordeaux, France",
            "crop_type": "stevia",
            "parameters": {
                "depth": 40,
                "importance_factors": {
                    "ph": 0.25,
                    "drainage": 0.35,
                    "texture": 0.2,
                    "organic_matter": 0.2
                }
            }
        },
        {
            "location": "Montpellier, France",
            "crop_type": "stevia",
            "parameters": {
                "depth": 35,
                "importance_factors": {
                    "ph": 0.3,
                    "drainage": 0.25,
                    "texture": 0.25,
                    "organic_matter": 0.2
                }
            }
        }
    ]
    
    return jsonify(examples)
