"""
Routes pour l'API d'analyse d'emplacement commercial.
"""
from flask import Blueprint, request, jsonify, render_template
from src.services.commercial_location_service import CommercialLocationService

# Création du blueprint
commercial_bp = Blueprint('commercial', __name__, url_prefix='/api/commercial')

# Initialisation du service
location_service = CommercialLocationService(use_mock=True)

@commercial_bp.route('/analyze', methods=['POST'])
def analyze_location():
    """
    Endpoint pour analyser un emplacement commercial.
    
    Exemple de requête:
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
    """
    data = request.json
    
    if not data or 'location' not in data:
        return jsonify({"error": "La localisation est requise"}), 400
    
    location = data.get('location')
    business_type = data.get('business_type', 'pharmacie')
    parameters = data.get('parameters', {})
    
    # Appel au service d'analyse
    results = location_service.analyze_location(location, business_type, parameters)
    
    # Transformation des chemins de fichiers en URLs relatives
    if 'visualizations' in results:
        for key, path in results['visualizations'].items():
            if path.startswith('src/static/'):
                results['visualizations'][key] = '/' + path.replace('src/static/', 'static/')
    
    return jsonify(results)

@commercial_bp.route('/examples', methods=['GET'])
def get_examples():
    """Renvoie des exemples de paramètres pour l'analyse d'emplacement commercial."""
    examples = [
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
        },
        {
            "location": "Lyon, France",
            "business_type": "pharmacie",
            "parameters": {
                "radius": 800,
                "importance_factors": {
                    "population": 0.3,
                    "competition": 0.4,
                    "accessibility": 0.3
                }
            }
        },
        {
            "location": "Toulouse, France",
            "business_type": "pharmacie",
            "parameters": {
                "radius": 600,
                "importance_factors": {
                    "population": 0.35,
                    "competition": 0.35,
                    "accessibility": 0.3
                }
            }
        }
    ]
    
    return jsonify(examples)
