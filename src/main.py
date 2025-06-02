"""
Point d'entrée principal de l'application Flask.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, send_from_directory, jsonify

def create_app():
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_geomarketing_ai')
    
    # Enregistrement des blueprints
    from src.routes.commercial_routes import commercial_bp
    from src.routes.soil_routes import soil_bp
    
    app.register_blueprint(commercial_bp)
    app.register_blueprint(soil_bp)
    
    # Route principale
    @app.route('/')
    def index():
        """Page d'accueil de l'application."""
        return render_template('index.html')
    
    # Route pour l'analyse d'emplacement commercial
    @app.route('/commercial')
    def commercial():
        """Page d'analyse d'emplacement commercial."""
        return render_template('commercial.html')
    
    # Route pour l'analyse de la qualité des sols
    @app.route('/soil')
    def soil():
        """Page d'analyse de la qualité des sols."""
        return render_template('soil.html')
    
    # Route pour la documentation
    @app.route('/docs')
    def docs():
        """Page de documentation de l'API."""
        return render_template('docs.html')
    
    # Route pour vérifier l'état de l'API
    @app.route('/api/health')
    def health_check():
        """Vérifie l'état de l'API."""
        return jsonify({"status": "ok", "version": "1.0.0"})
    
    # Gestion des erreurs
    @app.errorhandler(404)
    def page_not_found(e):
        """Gestion des erreurs 404."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        """Gestion des erreurs 500."""
        return render_template('500.html'), 500
    
    return app

# Si ce fichier est exécuté directement
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
