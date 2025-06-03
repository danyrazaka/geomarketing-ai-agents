"""
Routes utilisateur simplifiées sans dépendance à SQLAlchemy.
"""
from flask import Blueprint, request, jsonify, render_template
from src.models.user import User

# Créer un blueprint pour les routes utilisateur
user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    """
    Page de profil utilisateur (simulée).
    """
    # Créer un utilisateur de démonstration
    demo_user = User(
        user_id="user123",
        username="demo_user",
        email="demo@example.com"
    )
    
    return render_template('index.html', user=demo_user.to_dict())

@user_bp.route('/api/profile')
def get_profile():
    """
    API pour récupérer le profil utilisateur (simulé).
    """
    # Créer un utilisateur de démonstration
    demo_user = User(
        user_id="user123",
        username="demo_user",
        email="demo@example.com"
    )
    
    return jsonify(demo_user.to_dict())
