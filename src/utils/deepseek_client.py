"""
Module pour l'intégration avec DeepSeek R1.
Ce client permet d'utiliser l'IA DeepSeek R1 pour l'analyse géospatiale.
"""
import os
import json
import requests
from typing import Dict, Any, Optional, List, Union

class DeepseekClient:
    """
    Client pour l'API DeepSeek R1.
    """
    def __init__(self, api_key: Optional[str] = None, use_mock: bool = True):
        """
        Initialise le client DeepSeek R1.
        
        Args:
            api_key (str, optional): Clé API pour DeepSeek R1. Si non fournie, 
                                     utilise la variable d'environnement DEEPSEEK_API_KEY.
            use_mock (bool): Si True, utilise des réponses simulées au lieu d'appeler l'API réelle.
        """
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.api_url = "https://api.deepseek.com/v1"
        self.use_mock = use_mock
        
    def analyze_commercial_location(self, 
                                   location: str, 
                                   business_type: str, 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse un emplacement commercial à l'aide de DeepSeek R1.
        
        Args:
            location (str): Nom de l'emplacement (ville, adresse, etc.)
            business_type (str): Type de commerce (pharmacie, boulangerie, etc.)
            parameters (dict): Paramètres d'analyse (rayon, facteurs d'importance, etc.)
            
        Returns:
            dict: Résultats de l'analyse
        """
        if self.use_mock:
            return self._mock_commercial_location_response(location, business_type, parameters)
        
        # Construction de la requête pour l'API réelle
        prompt = self._build_commercial_location_prompt(location, business_type, parameters)
        
        # Appel à l'API DeepSeek R1
        response = self._call_api(prompt)
        
        # Traitement de la réponse
        return self._parse_commercial_location_response(response)
    
    def analyze_soil_quality(self, 
                            location: str, 
                            crop_type: str, 
                            parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse la qualité des sols à l'aide de DeepSeek R1.
        
        Args:
            location (str): Nom de l'emplacement (ville, région, etc.)
            crop_type (str): Type de culture (stevia, blé, etc.)
            parameters (dict): Paramètres d'analyse (profondeur, facteurs d'importance, etc.)
            
        Returns:
            dict: Résultats de l'analyse
        """
        if self.use_mock:
            return self._mock_soil_quality_response(location, crop_type, parameters)
        
        # Construction de la requête pour l'API réelle
        prompt = self._build_soil_quality_prompt(location, crop_type, parameters)
        
        # Appel à l'API DeepSeek R1
        response = self._call_api(prompt)
        
        # Traitement de la réponse
        return self._parse_soil_quality_response(response)
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """
        Appelle l'API DeepSeek R1.
        
        Args:
            prompt (str): Prompt à envoyer à l'API
            
        Returns:
            dict: Réponse de l'API
            
        Raises:
            Exception: En cas d'erreur lors de l'appel à l'API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-r1",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 2000
        }
        
        response = requests.post(
            f"{self.api_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Erreur lors de l'appel à l'API DeepSeek R1: {response.text}")
        
        return response.json()
    
    def _build_commercial_location_prompt(self, 
                                         location: str, 
                                         business_type: str, 
                                         parameters: Dict[str, Any]) -> str:
        """
        Construit le prompt pour l'analyse d'emplacement commercial.
        
        Args:
            location (str): Nom de l'emplacement
            business_type (str): Type de commerce
            parameters (dict): Paramètres d'analyse
            
        Returns:
            str: Prompt formaté
        """
        radius = parameters.get("radius", 500)
        importance_factors = parameters.get("importance_factors", {})
        
        prompt = f"""
        En tant qu'expert en géomarketing, analyse l'emplacement suivant pour y implanter un commerce:
        
        Localisation: {location}
        Type de commerce: {business_type}
        Rayon d'analyse: {radius} mètres
        
        Facteurs d'importance:
        - Population: {importance_factors.get('population', 0.4)}
        - Concurrence: {importance_factors.get('competition', 0.3)}
        - Accessibilité: {importance_factors.get('accessibility', 0.2)}
        - Visibilité: {importance_factors.get('visibility', 0.1)}
        
        Fournir une analyse détaillée avec:
        1. Scores d'attractivité (global, points d'intérêt, accessibilité, concurrence)
        2. Identification des emplacements optimaux avec leurs avantages et inconvénients
        3. Recommandations stratégiques
        
        Présenter les résultats sous forme de JSON structuré avec les clés suivantes:
        - scores: objet contenant les scores d'attractivité
        - hotspots: liste des emplacements optimaux avec leurs caractéristiques
        - recommendations: liste des recommandations stratégiques
        """
        
        return prompt
    
    def _build_soil_quality_prompt(self, 
                                  location: str, 
                                  crop_type: str, 
                                  parameters: Dict[str, Any]) -> str:
        """
        Construit le prompt pour l'analyse de la qualité des sols.
        
        Args:
            location (str): Nom de l'emplacement
            crop_type (str): Type de culture
            parameters (dict): Paramètres d'analyse
            
        Returns:
            str: Prompt formaté
        """
        depth = parameters.get("depth", 30)
        importance_factors = parameters.get("importance_factors", {})
        
        prompt = f"""
        En tant qu'expert en agronomie et pédologie, analyse la qualité des sols suivants pour la culture:
        
        Localisation: {location}
        Type de culture: {crop_type}
        Profondeur d'analyse: {depth} cm
        
        Facteurs d'importance:
        - pH: {importance_factors.get('ph', 0.3)}
        - Drainage: {importance_factors.get('drainage', 0.3)}
        - Texture: {importance_factors.get('texture', 0.2)}
        - Matière organique: {importance_factors.get('organic_matter', 0.2)}
        
        Fournir une analyse détaillée avec:
        1. Scores de compatibilité (global, pH, drainage, texture, matière organique)
        2. Identification des zones optimales, intermédiaires et peu adaptées
        3. Recommandations agronomiques pour chaque zone
        
        Présenter les résultats sous forme de JSON structuré avec les clés suivantes:
        - compatibility: objet contenant les scores de compatibilité
        - zones: liste des zones identifiées avec leurs caractéristiques
        - recommendations: liste des recommandations agronomiques
        """
        
        return prompt
    
    def _parse_commercial_location_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse la réponse de l'API pour l'analyse d'emplacement commercial.
        
        Args:
            response (dict): Réponse de l'API
            
        Returns:
            dict: Résultats structurés
        """
        try:
            content = response["choices"][0]["message"]["content"]
            # Extraire le JSON de la réponse
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            json_str = content[json_start:json_end]
            
            return json.loads(json_str)
        except (KeyError, json.JSONDecodeError, ValueError) as e:
            print(f"Erreur lors du parsing de la réponse: {e}")
            return {
                "error": "Impossible de parser la réponse de l'API",
                "raw_response": response
            }
    
    def _parse_soil_quality_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse la réponse de l'API pour l'analyse de la qualité des sols.
        
        Args:
            response (dict): Réponse de l'API
            
        Returns:
            dict: Résultats structurés
        """
        try:
            content = response["choices"][0]["message"]["content"]
            # Extraire le JSON de la réponse
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            json_str = content[json_start:json_end]
            
            return json.loads(json_str)
        except (KeyError, json.JSONDecodeError, ValueError) as e:
            print(f"Erreur lors du parsing de la réponse: {e}")
            return {
                "error": "Impossible de parser la réponse de l'API",
                "raw_response": response
            }
    
    def _mock_commercial_location_response(self, 
                                          location: str, 
                                          business_type: str, 
                                          parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère une réponse simulée pour l'analyse d'emplacement commercial.
        
        Args:
            location (str): Nom de l'emplacement
            business_type (str): Type de commerce
            parameters (dict): Paramètres d'analyse
            
        Returns:
            dict: Réponse simulée
        """
        # Ajuster légèrement les scores en fonction des paramètres
        radius = parameters.get("radius", 500)
        importance_factors = parameters.get("importance_factors", {})
        
        # Facteur de variation basé sur le rayon (plus le rayon est grand, plus le score est bas)
        radius_factor = 1.0 - (radius - 500) / 1000 if radius > 500 else 1.0 + (500 - radius) / 1000
        radius_factor = max(0.8, min(1.2, radius_factor))
        
        # Scores de base
        poi_score = 8.5 * radius_factor
        road_score = 7.2 * radius_factor
        competition_score = 5.0 * radius_factor
        
        # Ajustement en fonction des facteurs d'importance
        pop_factor = importance_factors.get("population", 0.4)
        comp_factor = importance_factors.get("competition", 0.3)
        acc_factor = importance_factors.get("accessibility", 0.2)
        vis_factor = importance_factors.get("visibility", 0.1)
        
        # Score global ajusté
        global_score = (
            poi_score * pop_factor + 
            road_score * acc_factor + 
            competition_score * comp_factor +
            (poi_score + road_score) / 2 * vis_factor
        )
        
        # Arrondir les scores à 1 décimale
        global_score = round(global_score, 1)
        poi_score = round(poi_score, 1)
        road_score = round(road_score, 1)
        competition_score = round(competition_score, 1)
        
        return {
            "location": location,
            "business_type": business_type,
            "analysis_results": {
                "poi_counts": {
                    "pharmacy": 5,
                    "hospital": 2,
                    "school": 8,
                    "supermarket": 6,
                    "bus_stop": 15
                },
                "road_density": 0.015,
                "competitors": 5,
                "score": {
                    "poi_score": poi_score,
                    "road_score": road_score,
                    "competition_score": competition_score,
                    "global_score": global_score
                }
            },
            "ai_recommendations": {
                "location": location,
                "analysis": f"Analyse d'emplacement commercial pour {location}:\n\nAprès analyse des données démographiques, des flux de circulation et de la concurrence, voici mes recommandations:\n\n1. Emplacement optimal: Le secteur nord-est de la zone présente le meilleur potentiel avec un score d'attractivité de 8.7/10.\n   - Avantages: Forte densité de population (environ 5000 habitants dans un rayon de 500m), proximité d'un centre médical, bon accès aux transports en commun.\n   - Inconvénients: Présence d'un concurrent à 800m, stationnement limité.\n\n2. Emplacement alternatif: Le carrefour central avec un score d'attractivité de 7.9/10.\n   - Avantages: Excellente visibilité, fort passage piétonnier (environ 1200 personnes/heure), synergie avec commerces existants.\n   - Inconvénients: Loyer potentiellement plus élevé, concurrence plus forte.\n\n3. Emplacement de niche: La zone résidentielle sud avec un score de 7.2/10.\n   - Avantages: Faible concurrence, population vieillissante (bon marché pour une pharmacie), stationnement facile.\n   - Inconvénients: Moindre visibilité, accès limité en transports en commun.\n\nJe recommande de privilégier le premier emplacement qui offre le meilleur équilibre entre accessibilité, visibilité et potentiel commercial.",
                "recommendations": [
                    "Je recommande de privilégier le premier emplacement qui offre le meilleur équilibre entre accessibilité, visibilité et potentiel commercial."
                ],
                "score": {
                    "emplacement_1": 8.7,
                    "emplacement_2": 7.9,
                    "emplacement_3": 7.2
                }
            },
            "visualizations": {
                "map": "/static/visualizations/location_map.html",
                "heatmap": "/static/visualizations/location_heatmap.png"
            }
        }
    
    def _mock_soil_quality_response(self, 
                                   location: str, 
                                   crop_type: str, 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère une réponse simulée pour l'analyse de la qualité des sols.
        
        Args:
            location (str): Nom de l'emplacement
            crop_type (str): Type de culture
            parameters (dict): Paramètres d'analyse
            
        Returns:
            dict: Réponse simulée
        """
        # Ajuster légèrement les scores en fonction des paramètres
        depth = parameters.get("depth", 30)
        importance_factors = parameters.get("importance_factors", {})
        
        # Facteur de variation basé sur la profondeur (plus la profondeur est grande, plus le score est précis)
        depth_factor = 1.0 + (depth - 30) / 100 if depth > 30 else 1.0 - (30 - depth) / 100
        depth_factor = max(0.9, min(1.1, depth_factor))
        
        # Scores de base
        ph_score = 8.5 * depth_factor
        drainage_score = 9.0 * depth_factor
        texture_score = 8.0 * depth_factor
        organic_score = 7.6 * depth_factor
        
        # Ajustement en fonction des facteurs d'importance
        ph_factor = importance_factors.get("ph", 0.3)
        drainage_factor = importance_factors.get("drainage", 0.3)
        texture_factor = importance_factors.get("texture", 0.2)
        organic_factor = importance_factors.get("organic_matter", 0.2)
        
        # Score global ajusté
        global_score = (
            ph_score * ph_factor + 
            drainage_score * drainage_factor + 
            texture_score * texture_factor +
            organic_score * organic_factor
        )
        
        # Arrondir les scores à 1 décimale
        global_score = round(global_score, 1)
        ph_score = round(ph_score, 1)
        drainage_score = round(drainage_score, 1)
        texture_score = round(texture_score, 1)
        organic_score = round(organic_score, 1)
        
        return {
            "location": location,
            "crop_type": crop_type,
            "analysis_results": {
                "soil_properties": {
                    "texture": "limoneux-sableux",
                    "ph": 6.5,
                    "organic_matter": 2.8,
                    "drainage": "bon",
                    "depth": "profond (>60cm)",
                    "water_retention": "moyenne"
                },
                "compatibility": {
                    "ph_score": ph_score,
                    "drainage_score": drainage_score,
                    "texture_score": texture_score,
                    "organic_score": organic_score,
                    "global_score": global_score
                },
                "zones": [
                    {
                        "name": "Zone optimale",
                        "proportion": 40,
                        "score": 8.7,
                        "color": "green"
                    },
                    {
                        "name": "Zone intermédiaire",
                        "proportion": 35,
                        "score": 6.5,
                        "color": "yellow"
                    },
                    {
                        "name": "Zone peu adaptée",
                        "proportion": 25,
                        "score": 4.2,
                        "color": "red"
                    }
                ]
            },
            "ai_recommendations": {
                "location": location,
                "crop_type": crop_type,
                "analysis": f"Analyse de la qualité des sols pour {location} concernant la culture de {crop_type}:\n\nAprès analyse des données pédologiques, climatiques et hydrologiques, voici mes conclusions:\n\n1. Zone optimale: La partie sud-est de la parcelle (environ 40% de la surface totale) présente les meilleures conditions.\n   - Caractéristiques: Sol limoneux-sableux, pH 6.2-6.8 (légèrement acide, idéal pour la stevia), bonne capacité de drainage.\n   - Recommandations: Aucun amendement majeur nécessaire, système d'irrigation goutte-à-goutte recommandé.\n\n2. Zone intermédiaire: La partie centrale (environ 35% de la surface).\n   - Caractéristiques: Sol plus argileux, pH 5.8-6.2 (un peu trop acide), drainage moyen.\n   - Recommandations: Amendement calcaire léger (500kg/ha), amélioration du drainage par sous-solage.\n\n3. Zone peu adaptée: La partie nord-ouest (environ 25% de la surface).\n   - Caractéristiques: Sol lourd et compacté, pH 5.5 (trop acide), risque d'engorgement.\n   - Recommandations: Utiliser pour d'autres cultures ou réaliser des travaux importants (drainage, amendements organiques et calcaires).\n\nPour maximiser le rendement de stevia, je recommande de concentrer la culture sur les zones 1 et 2, avec les amendements appropriés pour la zone 2. La zone 3 pourrait être réservée à d'autres cultures moins sensibles aux conditions acides et à l'engorgement.",
                "zones": [
                    {
                        "name": "Zone optimale",
                        "proportion": 40,
                        "characteristics": ["Sol limoneux-sableux", "pH 6.2-6.8", "Bonne capacité de drainage"],
                        "recommendations": ["Aucun amendement majeur nécessaire", "Système d'irrigation goutte-à-goutte recommandé"]
                    },
                    {
                        "name": "Zone intermédiaire",
                        "proportion": 35,
                        "characteristics": ["Sol plus argileux", "pH 5.8-6.2", "Drainage moyen"],
                        "recommendations": ["Amendement calcaire léger (500kg/ha)", "Amélioration du drainage par sous-solage"]
                    },
                    {
                        "name": "Zone peu adaptée",
                        "proportion": 25,
                        "characteristics": ["Sol lourd et compacté", "pH 5.5", "Risque d'engorgement"],
                        "recommendations": ["Utiliser pour d'autres cultures", "Ou réaliser des travaux importants (drainage, amendements)"]
                    }
                ],
                "recommendations": [
                    "Pour maximiser le rendement de stevia, je recommande de concentrer la culture sur les zones 1 et 2, avec les amendements appropriés pour la zone 2.",
                    "La zone 3 pourrait être réservée à d'autres cultures moins sensibles aux conditions acides et à l'engorgement."
                ]
            },
            "visualizations": {
                "map": "/static/visualizations/soil_map.html",
                "soil_map": "/static/visualizations/soil_quality_map.png"
            }
        }
