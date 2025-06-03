"""
Modèle pour les résultats d'analyse et les recommandations.
"""
from datetime import datetime

class AnalysisResult:
    """
    Modèle représentant les résultats d'une analyse géomarketing.
    """
    def __init__(self, result_id=None, analysis_type="", created_at=None):
        """
        Initialise un nouveau résultat d'analyse.
        
        Args:
            result_id (str): Identifiant unique du résultat
            analysis_type (str): Type d'analyse ('commercial' ou 'soil')
            created_at (datetime): Date de création du résultat
        """
        self.result_id = result_id or f"result_{int(datetime.now().timestamp())}"
        self.analysis_type = analysis_type
        self.created_at = created_at or datetime.now()
        self.scores = {}
        self.recommendations = []
        self.visualizations = {}
        self.raw_data = {}
    
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire.
        
        Returns:
            dict: Représentation dictionnaire de l'objet
        """
        return {
            "result_id": self.result_id,
            "analysis_type": self.analysis_type,
            "created_at": self.created_at.isoformat(),
            "scores": self.scores,
            "recommendations": self.recommendations,
            "visualizations": self.visualizations,
            "raw_data": self.raw_data
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données
            
        Returns:
            AnalysisResult: Instance créée
        """
        instance = cls(
            result_id=data.get("result_id"),
            analysis_type=data.get("analysis_type", "")
        )
        
        if "scores" in data:
            instance.scores = data["scores"]
        
        if "recommendations" in data:
            instance.recommendations = data["recommendations"]
            
        if "visualizations" in data:
            instance.visualizations = data["visualizations"]
            
        if "raw_data" in data:
            instance.raw_data = data["raw_data"]
            
        return instance
    
    def add_score(self, name, value):
        """
        Ajoute un score au résultat.
        
        Args:
            name (str): Nom du score
            value (float): Valeur du score
        """
        self.scores[name] = value
        
    def add_recommendation(self, recommendation):
        """
        Ajoute une recommandation au résultat.
        
        Args:
            recommendation (str): Texte de la recommandation
        """
        self.recommendations.append(recommendation)
        
    def add_visualization(self, name, path):
        """
        Ajoute une visualisation au résultat.
        
        Args:
            name (str): Nom de la visualisation
            path (str): Chemin vers la visualisation
        """
        self.visualizations[name] = path
        
    def add_raw_data(self, name, data):
        """
        Ajoute des données brutes au résultat.
        
        Args:
            name (str): Nom des données
            data (any): Données à ajouter
        """
        self.raw_data[name] = data
