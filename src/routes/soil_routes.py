"""
Routes pour l'API d'analyse de la qualité des sols.
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import json
from src.services.soil_quality_service import SoilQualityService
from src.models.soil_quality import SoilQuality

# Créer un blueprint pour les routes d'analyse des sols
soil_bp = Blueprint('soil', __name__)

# Initialiser le service
soil_service = SoilQualityService(use_mock=True)

@soil_bp.route('/')
def index():
    """
    Page principale d'analyse de la qualité des sols.
    """
    return render_template('soil.html')

@soil_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint pour analyser la qualité des sols.
    """
    try:
        # Récupérer les données du formulaire
        data = request.form if request.form else request.get_json()
        
        # Créer un objet SoilQuality
        soil = SoilQuality(
            location_name=data.get('location', ''),
            crop_type=data.get('crop_type', ''),
            depth=int(data.get('depth', 30))
        )
        
        # Récupérer les facteurs d'importance
        importance_factors = {
            'ph': float(data.get('ph_factor', 0.3)),
            'drainage': float(data.get('drainage_factor', 0.3)),
            'texture': float(data.get('texture_factor', 0.2)),
            'organic_matter': float(data.get('organic_matter_factor', 0.2))
        }
        soil.importance_factors = importance_factors
        
        # Analyser le sol
        result = soil_service.analyze_soil(soil)
        
        # Si la requête vient de l'API, renvoyer un JSON
        if request.is_json:
            return jsonify(result.to_dict())
        
        # Sinon, rediriger vers la page de résultats
        return render_template('soil.html', 
                              soil=soil.to_dict(), 
                              result=result.to_dict(),
                              active_tab='results')
        
    except Exception as e:
        error_message = f"Erreur lors de l'analyse: {str(e)}"
        if request.is_json:
            return jsonify({'error': error_message}), 500
        return render_template('soil.html', error=error_message)

@soil_bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    Endpoint API pour analyser la qualité des sols.
    """
    try:
        # Récupérer les données JSON
        data = request.get_json()
        
        # Créer un objet SoilQuality
        soil = SoilQuality(
            location_name=data.get('location', ''),
            crop_type=data.get('crop_type', ''),
            depth=data.get('parameters', {}).get('depth', 30)
        )
        
        # Récupérer les facteurs d'importance
        importance_factors = data.get('parameters', {}).get('importance_factors', {})
        if importance_factors:
            soil.importance_factors = importance_factors
        
        # Analyser le sol
        result = soil_service.analyze_soil(soil)
        
        # Renvoyer les résultats
        return jsonify(result.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@soil_bp.route('/example')
def load_example():
    """
    Charge un exemple d'analyse.
    """
    # Créer un exemple de sol
    soil = SoilQuality(
        location_name="Toulouse, France",
        crop_type="Stevia",
        depth=30
    )
    
    # Analyser le sol
    result = soil_service.analyze_soil(soil)
    
    # Renvoyer la page avec les résultats
    return render_template('soil.html', 
                          soil=soil.to_dict(), 
                          result=result.to_dict(),
                          active_tab='results')
