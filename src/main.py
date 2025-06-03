"""
Point d'entrée principal de l'application Flask.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, request, jsonify
from src.routes.commercial_routes import commercial_bp
from src.routes.soil_routes import soil_bp
from src.routes.user import user_bp

# Créer l'application Flask
app = Flask(__name__)

# Enregistrer les blueprints
app.register_blueprint(commercial_bp, url_prefix='/commercial')
app.register_blueprint(soil_bp, url_prefix='/soil')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def index():
    """
    Page d'accueil de l'application.
    """
    return render_template('index.html')

@app.route('/docs')
def docs():
    """
    Page de documentation de l'application.
    """
    return render_template('docs.html')

@app.errorhandler(404)
def page_not_found(e):
    """
    Gestionnaire d'erreur 404.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Gestionnaire d'erreur 500.
    """
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Démarrer l'application en mode debug
    app.run(host='0.0.0.0', port=5000, debug=True)
