"""
Module pour l'intégration avec DeepSeek-R1 ou un mock pour le développement local.
"""
import os
import json
import requests
from typing import Dict, Any, Optional, List

class DeepSeekClient:
    """
    Client pour interagir avec l'API DeepSeek-R1 ou utiliser un mock local.
    """
    def __init__(self, use_mock: bool = True, api_key: Optional[str] = None):
        """
        Initialise le client DeepSeek.
        
        Args:
            use_mock: Si True, utilise un mock local au lieu de l'API réelle
            api_key: Clé API pour DeepSeek-R1 (nécessaire si use_mock=False)
        """
        self.use_mock = use_mock
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # URL fictive, à remplacer par l'URL réelle
        
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Génère une réponse basée sur un prompt et un contexte optionnel.
        
        Args:
            prompt: Le prompt à envoyer à DeepSeek-R1
            context: Contexte supplémentaire pour guider la génération
            
        Returns:
            La réponse générée
        """
        if self.use_mock:
            return self._mock_response(prompt, context)
        
        # Vérification de la clé API
        if not self.api_key:
            raise ValueError("API key is required when not using mock")
        
        # Préparation des données pour l'API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-r1-distill-qwen-32b",
            "messages": [
                {"role": "system", "content": "Vous êtes un assistant spécialisé en géomarketing qui aide à analyser des données géospatiales."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        # Ajout du contexte si fourni
        if context:
            data["messages"].insert(1, {"role": "system", "content": json.dumps(context)})
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error calling DeepSeek API: {e}")
            return "Une erreur s'est produite lors de la communication avec l'API DeepSeek."
    
    def _mock_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Génère une réponse mock basée sur des règles prédéfinies.
        
        Args:
            prompt: Le prompt envoyé
            context: Contexte supplémentaire
            
        Returns:
            Une réponse simulée
        """
        # Analyse du prompt pour déterminer le type de requête
        if "emplacement" in prompt.lower() or "pharmacie" in prompt.lower() or "commercial" in prompt.lower():
            return self._mock_commercial_location(prompt, context)
        elif "sol" in prompt.lower() or "stevia" in prompt.lower() or "culture" in prompt.lower():
            return self._mock_soil_quality(prompt, context)
        else:
            return "Je ne peux pas déterminer le type d'analyse demandée. Veuillez préciser si vous souhaitez une analyse d'emplacement commercial ou de qualité des sols."
    
    def _mock_commercial_location(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Mock pour les réponses d'optimisation d'emplacement commercial"""
        location = context.get("location", "la zone sélectionnée") if context else "la zone sélectionnée"
        
        return f"""Analyse d'emplacement commercial pour {location}:

Après analyse des données démographiques, des flux de circulation et de la concurrence, voici mes recommandations:

1. Emplacement optimal: Le secteur nord-est de la zone présente le meilleur potentiel avec un score d'attractivité de 8.7/10.
   - Avantages: Forte densité de population (environ 5000 habitants dans un rayon de 500m), proximité d'un centre médical, bon accès aux transports en commun.
   - Inconvénients: Présence d'un concurrent à 800m, stationnement limité.

2. Emplacement alternatif: Le carrefour central avec un score d'attractivité de 7.9/10.
   - Avantages: Excellente visibilité, fort passage piétonnier (environ 1200 personnes/heure), synergie avec commerces existants.
   - Inconvénients: Loyer potentiellement plus élevé, concurrence plus forte.

3. Emplacement de niche: La zone résidentielle sud avec un score de 7.2/10.
   - Avantages: Faible concurrence, population vieillissante (bon marché pour une pharmacie), stationnement facile.
   - Inconvénients: Moindre visibilité, accès limité en transports en commun.

Je recommande de privilégier le premier emplacement qui offre le meilleur équilibre entre accessibilité, visibilité et potentiel commercial.
"""
    
    def _mock_soil_quality(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Mock pour les réponses d'analyse de qualité des sols"""
        location = context.get("location", "la parcelle sélectionnée") if context else "la parcelle sélectionnée"
        
        return f"""Analyse de la qualité des sols pour {location} concernant la culture de stevia:

Après analyse des données pédologiques, climatiques et hydrologiques, voici mes conclusions:

1. Zone optimale: La partie sud-est de la parcelle (environ 40% de la surface totale) présente les meilleures conditions.
   - Caractéristiques: Sol limoneux-sableux, pH 6.2-6.8 (légèrement acide, idéal pour la stevia), bonne capacité de drainage.
   - Recommandations: Aucun amendement majeur nécessaire, système d'irrigation goutte-à-goutte recommandé.

2. Zone intermédiaire: La partie centrale (environ 35% de la surface).
   - Caractéristiques: Sol plus argileux, pH 5.8-6.2 (un peu trop acide), drainage moyen.
   - Recommandations: Amendement calcaire léger (500kg/ha), amélioration du drainage par sous-solage.

3. Zone peu adaptée: La partie nord-ouest (environ 25% de la surface).
   - Caractéristiques: Sol lourd et compacté, pH 5.5 (trop acide), risque d'engorgement.
   - Recommandations: Utiliser pour d'autres cultures ou réaliser des travaux importants (drainage, amendements organiques et calcaires).

Pour maximiser le rendement de stevia, je recommande de concentrer la culture sur les zones 1 et 2, avec les amendements appropriés pour la zone 2. La zone 3 pourrait être réservée à d'autres cultures moins sensibles aux conditions acides et à l'engorgement.
"""

    def analyze_commercial_location(self, location: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse un emplacement commercial spécifique.
        
        Args:
            location: Nom ou coordonnées de l'emplacement
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats de l'analyse avec recommandations
        """
        prompt = f"""Analyser l'emplacement optimal pour une pharmacie dans la zone {location}.
Prendre en compte les facteurs suivants:
- Densité de population
- Flux de circulation
- Présence de concurrents
- Accessibilité
- Visibilité
"""
        
        if parameters:
            prompt += "\nParamètres spécifiques:\n"
            for key, value in parameters.items():
                prompt += f"- {key}: {value}\n"
        
        response = self.generate_response(prompt, {"location": location, "parameters": parameters})
        
        # Structuration de la réponse
        return {
            "location": location,
            "analysis": response,
            "recommendations": self._extract_recommendations(response),
            "score": self._extract_score(response)
        }
    
    def analyze_soil_quality(self, location: str, crop_type: str = "stevia", parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyse la qualité des sols pour une culture spécifique.
        
        Args:
            location: Nom ou coordonnées de la parcelle
            crop_type: Type de culture (par défaut: stevia)
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats de l'analyse avec recommandations
        """
        prompt = f"""Analyser la qualité des sols pour la culture de {crop_type} dans la parcelle située à {location}.
Prendre en compte les facteurs suivants:
- Texture et structure du sol
- pH et composition chimique
- Drainage et capacité de rétention d'eau
- Conditions climatiques locales
"""
        
        if parameters:
            prompt += "\nParamètres spécifiques:\n"
            for key, value in parameters.items():
                prompt += f"- {key}: {value}\n"
        
        response = self.generate_response(prompt, {"location": location, "crop_type": crop_type, "parameters": parameters})
        
        # Structuration de la réponse
        return {
            "location": location,
            "crop_type": crop_type,
            "analysis": response,
            "zones": self._extract_zones(response),
            "recommendations": self._extract_recommendations(response)
        }
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extrait les recommandations d'un texte"""
        recommendations = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if "recommand" in line.lower():
                recommendations.append(line)
                # Ajouter aussi la ligne suivante si elle existe et n'est pas vide
                if i+1 < len(lines) and lines[i+1].strip():
                    recommendations.append(lines[i+1])
        
        return recommendations if recommendations else ["Pas de recommandations spécifiques identifiées."]
    
    def _extract_score(self, text: str) -> Dict[str, float]:
        """Extrait les scores d'attractivité d'un texte"""
        scores = {}
        import re
        
        # Recherche des patterns comme "score d'attractivité de 8.7/10"
        score_patterns = re.finditer(r"score\s+d[e']attractivit[ée]\s+de\s+(\d+\.\d+)\/10", text, re.IGNORECASE)
        
        for i, match in enumerate(score_patterns):
            scores[f"emplacement_{i+1}"] = float(match.group(1))
        
        return scores if scores else {"score_global": 5.0}  # Valeur par défaut
    
    def _extract_zones(self, text: str) -> List[Dict[str, Any]]:
        """Extrait les informations sur les zones de qualité des sols"""
        zones = []
        lines = text.split('\n')
        current_zone = None
        
        for line in lines:
            if "Zone" in line and ":" in line:
                if current_zone:
                    zones.append(current_zone)
                
                # Extraire le type de zone et sa proportion
                import re
                proportion_match = re.search(r"\(environ\s+(\d+)%", line)
                proportion = int(proportion_match.group(1)) if proportion_match else None
                
                current_zone = {
                    "name": line.split(":")[0].strip(),
                    "description": line.split(":")[1].strip(),
                    "proportion": proportion,
                    "characteristics": [],
                    "recommendations": []
                }
            elif current_zone and "Caractéristiques:" in line:
                current_zone["characteristics"].append(line.replace("Caractéristiques:", "").strip())
            elif current_zone and "Recommandations:" in line:
                current_zone["recommendations"].append(line.replace("Recommandations:", "").strip())
        
        # Ajouter la dernière zone
        if current_zone:
            zones.append(current_zone)
        
        return zones if zones else [{"name": "Zone unique", "proportion": 100, "characteristics": [], "recommendations": []}]
