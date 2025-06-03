"""
Module utilisateur simplifié sans dépendance à SQLAlchemy.
"""

class User:
    """
    Modèle utilisateur simplifié pour la démonstration.
    """
    def __init__(self, user_id=None, username="", email=""):
        """
        Initialise un nouvel utilisateur.
        
        Args:
            user_id (str): Identifiant unique de l'utilisateur
            username (str): Nom d'utilisateur
            email (str): Adresse email
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire.
        
        Returns:
            dict: Représentation dictionnaire de l'objet
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email
        }
