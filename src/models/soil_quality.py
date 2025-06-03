"""
Modèle pour les analyses de qualité des sols.
"""
from datetime import datetime

class SoilQuality:
    """
    Modèle représentant une analyse de qualité des sols.
    """
    def __init__(self, soil_id=None, location_name="", crop_type="", 
                 latitude=0.0, longitude=0.0, depth=30, created_at=None):
        """
        Initialise une nouvelle analyse de qualité des sols.
        
        Args:
            soil_id (str): Identifiant unique de l'analyse
            location_name (str): Nom de l'emplacement (ville, région, etc.)
            crop_type (str): Type de culture (stevia, blé, etc.)
            latitude (float): Latitude de l'emplacement
            longitude (float): Longitude de l'emplacement
            depth (int): Profondeur d'analyse en cm
            created_at (datetime): Date de création de l'analyse
        """
        self.soil_id = soil_id or f"soil_{int(datetime.now().timestamp())}"
        self.location_name = location_name
        self.crop_type = crop_type
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.created_at = created_at or datetime.now()
        self.importance_factors = {
            "ph": 0.3,
            "drainage": 0.3,
            "texture": 0.2,
            "organic_matter": 0.2
        }
        self.results = None
    
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire.
        
        Returns:
            dict: Représentation dictionnaire de l'objet
        """
        return {
            "soil_id": self.soil_id,
            "location_name": self.location_name,
            "crop_type": self.crop_type,
            "coordinates": {
                "latitude": self.latitude,
                "longitude": self.longitude
            },
            "depth": self.depth,
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
            SoilQuality: Instance créée
        """
        instance = cls(
            soil_id=data.get("soil_id"),
            location_name=data.get("location_name", ""),
            crop_type=data.get("crop_type", ""),
            latitude=data.get("coordinates", {}).get("latitude", 0.0),
            longitude=data.get("coordinates", {}).get("longitude", 0.0),
            depth=data.get("depth", 30)
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
        
    def get_compatibility_score(self):
        """
        Récupère le score de compatibilité global de l'analyse.
        
        Returns:
            float: Score de compatibilité ou None si pas de résultats
        """
        if not self.results or "compatibility" not in self.results:
            return None
        
        return self.results["compatibility"].get("global_score")
