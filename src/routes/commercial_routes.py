"""
Routes pour l'API d'analyse d'emplacements commerciaux.
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import json
from src.services.commercial_location_service import CommercialLocationService
from src.models.commercial_location import CommercialLocation

# Créer un blueprint pour les routes commerciales
commercial_bp = Blueprint('commercial', __name__)

# Initialiser le service
commercial_service = CommercialLocationService(use_mock=True)

@commercial_bp.route('/')
def index():
    """
    Page principale d'analyse d'emplacement commercial.
    """
    return render_template('commercial.html')

@commercial_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint pour analyser un emplacement commercial.
    """
    try:
        # Récupérer les données du formulaire
        data = request.form if request.form else request.get_json()
        
        # Créer un objet CommercialLocation
        location = CommercialLocation(
            location_name=data.get('location', ''),
            business_type=data.get('business_type', ''),
            radius=int(data.get('radius', 500))
        )
        
        # Récupérer les facteurs d'importance
        importance_factors = {
            'population': float(data.get('population_factor', 0.4)),
            'competition': float(data.get('competition_factor', 0.3)),
            'accessibility': float(data.get('accessibility_factor', 0.2)),
            'visibility': float(data.get('visibility_factor', 0.1))
        }
        location.importance_factors = importance_factors
        
        # Analyser l'emplacement
        result = commercial_service.analyze_location(location)
        
        # Si la requête vient de l'API, renvoyer un JSON
        if request.is_json:
            return jsonify(result.to_dict())
        
        # Sinon, rediriger vers la page de résultats
        return render_template('commercial.html', 
                              location=location.to_dict(), 
                              result=result.to_dict(),
                              active_tab='results')
        
    except Exception as e:
        error_message = f"Erreur lors de l'analyse: {str(e)}"
        if request.is_json:
            return jsonify({'error': error_message}), 500
        return render_template('commercial.html', error=error_message)

@commercial_bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    Endpoint API pour analyser un emplacement commercial.
    """
    try:
        # Récupérer les données JSON
        data = request.get_json()
        
        # Créer un objet CommercialLocation
        location = CommercialLocation(
            location_name=data.get('location', ''),
            business_type=data.get('business_type', ''),
            radius=data.get('parameters', {}).get('radius', 500)
        )
        
        # Récupérer les facteurs d'importance
        importance_factors = data.get('parameters', {}).get('importance_factors', {})
        if importance_factors:
            location.importance_factors = importance_factors
        
        # Analyser l'emplacement
        result = commercial_service.analyze_location(location)
        
        # Renvoyer les résultats
        return jsonify(result.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@commercial_bp.route('/example')
def load_example():
    """
    Charge un exemple d'analyse.
    """
    # Créer un exemple d'emplacement
    location = CommercialLocation(
        location_name="Paris, France",
        business_type="Pharmacie",
        radius=500
    )
    
    # Analyser l'emplacement
    result = commercial_service.analyze_location(location)
    
    # Renvoyer la page avec les résultats
    return render_template('commercial.html', 
                          location=location.to_dict(), 
                          result=result.to_dict(),
                          active_tab='results')
