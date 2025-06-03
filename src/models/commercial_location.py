"""
Modèle pour les analyses d'emplacement commercial.
"""
from datetime import datetime

class CommercialLocation:
    """
    Modèle représentant une analyse d'emplacement commercial.
    """
    def __init__(self, location_id=None, location_name="", business_type="", 
                 latitude=0.0, longitude=0.0, radius=500, created_at=None):
        """
        Initialise une nouvelle analyse d'emplacement commercial.
        
        Args:
            location_id (str): Identifiant unique de l'emplacement
            location_name (str): Nom de l'emplacement (ville, adresse, etc.)
            business_type (str): Type de commerce (pharmacie, boulangerie, etc.)
            latitude (float): Latitude de l'emplacement
            longitude (float): Longitude de l'emplacement
            radius (int): Rayon d'analyse en mètres
            created_at (datetime): Date de création de l'analyse
        """
        self.location_id = location_id or f"loc_{int(datetime.now().timestamp())}"
        self.location_name = location_name
        self.business_type = business_type
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.created_at = created_at or datetime.now()
        self.importance_factors = {
            "population": 0.4,
            "competition": 0.3,
            "accessibility": 0.2,
            "visibility": 0.1
        }
        self.results = None
    
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire.
        
        Returns:
            dict: Représentation dictionnaire de l'objet
        """
        return {
            "location_id": self.location_id,
            "location_name": self.location_name,
            "business_type": self.business_type,
            "coordinates": {
                "latitude": self.latitude,
                "longitude": self.longitude
            },
            "radius": self.radius,
            "importance_factors": self.importance_factors,
            "created_at": self.created_at.isoformat(),
            "results": self.results
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données
            
        Returns:
            CommercialLocation: Instance créée
        """
        instance = cls(
            location_id=data.get("location_id"),
            location_name=data.get("location_name", ""),
            business_type=data.get("business_type", ""),
            latitude=data.get("coordinates", {}).get("latitude", 0.0),
            longitude=data.get("coordinates", {}).get("longitude", 0.0),
            radius=data.get("radius", 500)
        )
        
        if "importance_factors" in data:
            instance.importance_factors = data["importance_factors"]
        
        if "results" in data:
            instance.results = data["results"]
            
        return instance
    
    def set_results(self, results):
        """
        Définit les résultats de l'analyse.
        
        Args:
            results (dict): Résultats de l'analyse
        """
        self.results = results
        
    def get_score(self):
        """
        Récupère le score global de l'analyse.
        
        Returns:
            float: Score global ou None si pas de résultats
        """
        if not self.results or "score" not in self.results:
            return None
        
        return self.results["score"].get("global_score")
