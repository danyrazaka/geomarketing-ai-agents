"""
Service pour l'analyse de la qualité des sols.
"""
import os
import json
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List, Tuple
from src.utils.deepseek_client import DeepSeekClient

class SoilQualityService:
    """
    Service pour analyser la qualité des sols pour différentes cultures.
    """
    def __init__(self, use_mock: bool = True):
        """
        Initialise le service d'analyse de la qualité des sols.
        
        Args:
            use_mock: Si True, utilise des données mockées pour le développement
        """
        self.use_mock = use_mock
        self.ai_client = DeepSeekClient(use_mock=use_mock)
        
    def analyze_soil(self, location: str, crop_type: str = "stevia", 
                    parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyse la qualité des sols pour une culture spécifique.
        
        Args:
            location: Nom ou coordonnées de la parcelle (ex: "Toulouse, France")
            crop_type: Type de culture (ex: "stevia")
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats de l'analyse avec recommandations et visualisations
        """
        if self.use_mock:
            return self._mock_analysis(location, crop_type, parameters)
        
        # Récupération des données pédologiques
        try:
            # Récupérer les données de sol
            gdf_soil = self._get_soil_data(location)
            
            # Analyser les données
            analysis_results = self._analyze_soil_data(gdf_soil, crop_type, parameters)
            
            # Générer des visualisations
            map_path, soil_map_path = self._generate_visualizations(gdf_soil, analysis_results)
            
            # Obtenir des recommandations IA
            ai_recommendations = self.ai_client.analyze_soil_quality(
                location, 
                crop_type,
                parameters or {}
            )
            
            # Combiner les résultats
            return {
                "location": location,
                "crop_type": crop_type,
                "analysis_results": analysis_results,
                "ai_recommendations": ai_recommendations,
                "visualizations": {
                    "map": map_path,
                    "soil_map": soil_map_path
                }
            }
        except Exception as e:
            print(f"Error analyzing soil: {e}")
            return self._mock_analysis(location, crop_type, parameters)
    
    def _get_soil_data(self, location: str) -> gpd.GeoDataFrame:
        """
        Récupère les données pédologiques d'une zone.
        
        Args:
            location: Nom ou coordonnées de la parcelle
            
        Returns:
            GeoDataFrame contenant les données pédologiques
        """
        # Note: Dans une implémentation réelle, cette fonction récupérerait des données
        # depuis des sources comme l'INRAE ou la FAO. Pour ce prototype, nous utilisons
        # des données simulées.
        
        # Récupérer les limites de la zone
        area = gpd.GeoDataFrame()
        
        # Simuler des données pédologiques
        # Dans une implémentation réelle, ces données proviendraient de sources externes
        return {
            'area': area,
            'soil_data': gpd.GeoDataFrame()
        }
    
    def _analyze_soil_data(self, gdf_soil: Dict[str, gpd.GeoDataFrame], 
                          crop_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse les données pédologiques pour évaluer la compatibilité avec une culture.
        
        Args:
            gdf_soil: Dictionnaire de GeoDataFrames contenant les données pédologiques
            crop_type: Type de culture
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats de l'analyse
        """
        # Exemple d'analyse simple
        # Dans une implémentation réelle, cette fonction serait beaucoup plus complexe
        
        # Simuler des résultats d'analyse
        soil_properties = {
            "texture": "limoneux-sableux",
            "ph": 6.5,
            "organic_matter": 2.8,
            "drainage": "bon"
        }
        
        # Évaluer la compatibilité avec la culture spécifiée
        compatibility = self._evaluate_crop_compatibility(soil_properties, crop_type)
        
        return {
            'soil_properties': soil_properties,
            'compatibility': compatibility,
            'zones': self._identify_soil_zones(soil_properties, crop_type)
        }
    
    def _evaluate_crop_compatibility(self, soil_properties: Dict[str, Any], 
                                   crop_type: str) -> Dict[str, float]:
        """
        Évalue la compatibilité des propriétés du sol avec une culture spécifique.
        
        Args:
            soil_properties: Propriétés du sol
            crop_type: Type de culture
            
        Returns:
            Scores de compatibilité pour différents critères
        """
        # Exemple d'évaluation simple
        # Dans une implémentation réelle, cette fonction serait basée sur des
        # connaissances agronomiques spécifiques à chaque culture
        
        # Évaluation pour la stevia (exemple)
        if crop_type.lower() == "stevia":
            # pH optimal pour la stevia: 6.0-7.5
            ph = soil_properties.get("ph", 7.0)
            ph_score = 10 - min(abs(ph - 6.75) * 3, 10)
            
            # Drainage: la stevia préfère un bon drainage
            drainage = soil_properties.get("drainage", "moyen")
            drainage_score = {"bon": 9, "moyen": 6, "faible": 3}.get(drainage, 5)
            
            # Texture: la stevia préfère les sols limoneux-sableux
            texture = soil_properties.get("texture", "")
            texture_score = 8 if "limoneux" in texture and "sableux" in texture else 5
            
            # Matière organique: la stevia bénéficie d'une bonne teneur
            organic_matter = soil_properties.get("organic_matter", 2.0)
            organic_score = min(organic_matter * 2, 10)
            
            # Score global
            global_score = (ph_score * 0.3 + drainage_score * 0.3 + 
                           texture_score * 0.2 + organic_score * 0.2)
            
            return {
                "ph_score": round(ph_score, 1),
                "drainage_score": round(drainage_score, 1),
                "texture_score": round(texture_score, 1),
                "organic_score": round(organic_score, 1),
                "global_score": round(global_score, 1)
            }
        
        # Pour d'autres cultures, retourner des scores par défaut
        return {
            "global_score": 5.0,
            "details": "Analyse détaillée non disponible pour cette culture"
        }
    
    def _identify_soil_zones(self, soil_properties: Dict[str, Any], 
                           crop_type: str) -> List[Dict[str, Any]]:
        """
        Identifie différentes zones dans la parcelle selon leur aptitude.
        
        Args:
            soil_properties: Propriétés du sol
            crop_type: Type de culture
            
        Returns:
            Liste des zones identifiées avec leurs caractéristiques
        """
        # Exemple simple de zonage
        # Dans une implémentation réelle, cette fonction utiliserait des
        # algorithmes de clustering sur des données spatiales
        
        # Simuler trois zones avec différentes aptitudes
        return [
            {
                "name": "Zone optimale",
                "proportion": 40,
                "properties": {
                    "ph": 6.5,
                    "texture": "limoneux-sableux",
                    "drainage": "bon"
                },
                "score": 8.7,
                "recommendations": "Aucun amendement majeur nécessaire"
            },
            {
                "name": "Zone intermédiaire",
                "proportion": 35,
                "properties": {
                    "ph": 6.0,
                    "texture": "limoneux-argileux",
                    "drainage": "moyen"
                },
                "score": 6.5,
                "recommendations": "Amendement calcaire léger recommandé"
            },
            {
                "name": "Zone peu adaptée",
                "proportion": 25,
                "properties": {
                    "ph": 5.5,
                    "texture": "argileux",
                    "drainage": "faible"
                },
                "score": 4.2,
                "recommendations": "Nécessite des travaux importants ou changement de culture"
            }
        ]
    
    def _generate_visualizations(self, gdf_soil: Dict[str, gpd.GeoDataFrame], 
                               analysis_results: Dict[str, Any]) -> Tuple[str, str]:
        """
        Génère des visualisations pour les résultats de l'analyse.
        
        Args:
            gdf_soil: Dictionnaire de GeoDataFrames contenant les données pédologiques
            analysis_results: Résultats de l'analyse
            
        Returns:
            Chemins vers les fichiers de visualisation générés
        """
        # Créer un dossier pour les visualisations si nécessaire
        os.makedirs('src/static/visualizations', exist_ok=True)
        
        # Générer une carte interactive avec Folium
        map_path = 'src/static/visualizations/soil_map.html'
        
        # Carte par défaut (centrée sur la France)
        m = folium.Map(location=[46.2276, 2.2137], zoom_start=6)
        
        # Ajouter les zones si disponibles
        if 'zones' in analysis_results:
            # Dans une implémentation réelle, ces zones seraient basées sur des
            # géométries réelles. Ici, nous simulons des cercles pour l'exemple.
            colors = ['green', 'yellow', 'red']
            for i, zone in enumerate(analysis_results['zones']):
                if i < len(colors):
                    folium.Circle(
                        location=[46.2276 + i*0.01, 2.2137 + i*0.01],
                        radius=zone['proportion'] * 100,
                        color=colors[i],
                        fill=True,
                        fill_opacity=0.6,
                        popup=f"{zone['name']}: {zone['score']}/10"
                    ).add_to(m)
        
        # Sauvegarder la carte
        m.save(map_path)
        
        # Générer une carte de qualité des sols
        soil_map_path = 'src/static/visualizations/soil_quality_map.png'
        
        plt.figure(figsize=(10, 8))
        plt.title('Qualité des sols pour la culture')
        
        # Exemple simple de carte de qualité des sols
        # Dans une implémentation réelle, cette visualisation serait basée sur des données réelles
        x = np.linspace(0, 10, 20)
        y = np.linspace(0, 10, 20)
        X, Y = np.meshgrid(x, y)
        
        # Simuler différentes zones de qualité
        Z = np.zeros_like(X)
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                # Zone 1: optimale (coin supérieur gauche)
                if i < 10 and j < 10:
                    Z[i, j] = 8 + np.random.rand()
                # Zone 2: intermédiaire (centre)
                elif 5 <= i < 15 and 5 <= j < 15:
                    Z[i, j] = 6 + np.random.rand()
                # Zone 3: peu adaptée (coin inférieur droit)
                else:
                    Z[i, j] = 4 + np.random.rand()
        
        plt.contourf(X, Y, Z, cmap='RdYlGn', levels=10)
        plt.colorbar(label='Score de compatibilité')
        plt.xlabel('Est-Ouest')
        plt.ylabel('Nord-Sud')
        plt.savefig(soil_map_path)
        plt.close()
        
        return map_path, soil_map_path
    
    def _mock_analysis(self, location: str, crop_type: str, 
                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère une analyse mockée pour le développement et les tests.
        
        Args:
            location: Nom ou coordonnées de la parcelle
            crop_type: Type de culture
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats mockés de l'analyse
        """
        # Créer un dossier pour les visualisations si nécessaire
        os.makedirs('src/static/visualizations', exist_ok=True)
        
        # Générer une carte simple
        map_path = 'src/static/visualizations/soil_map.html'
        m = folium.Map(location=[43.6047, 1.4442], zoom_start=12)  # Toulouse
        
        # Ajouter des zones simulées
        zones = [
            {"name": "Zone optimale", "proportion": 40, "score": 8.7, "color": "green"},
            {"name": "Zone intermédiaire", "proportion": 35, "score": 6.5, "color": "yellow"},
            {"name": "Zone peu adaptée", "proportion": 25, "score": 4.2, "color": "red"}
        ]
        
        for i, zone in enumerate(zones):
            folium.Circle(
                location=[43.6047 + i*0.01, 1.4442 + i*0.01],
                radius=zone['proportion'] * 100,
                color=zone['color'],
                fill=True,
                fill_opacity=0.6,
                popup=f"{zone['name']}: {zone['score']}/10"
            ).add_to(m)
        
        m.save(map_path)
        
        # Générer une carte de qualité des sols
        soil_map_path = 'src/static/visualizations/soil_quality_map.png'
        
        plt.figure(figsize=(10, 8))
        plt.title(f'Qualité des sols pour la culture de {crop_type} (Données simulées)')
        
        x = np.linspace(0, 10, 20)
        y = np.linspace(0, 10, 20)
        X, Y = np.meshgrid(x, y)
        
        # Simuler différentes zones de qualité
        Z = np.zeros_like(X)
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                # Zone 1: optimale (coin supérieur gauche)
                if i < 10 and j < 10:
                    Z[i, j] = 8 + np.random.rand()
                # Zone 2: intermédiaire (centre)
                elif 5 <= i < 15 and 5 <= j < 15:
                    Z[i, j] = 6 + np.random.rand()
                # Zone 3: peu adaptée (coin inférieur droit)
                else:
                    Z[i, j] = 4 + np.random.rand()
        
        plt.contourf(X, Y, Z, cmap='RdYlGn', levels=10)
        plt.colorbar(label='Score de compatibilité')
        plt.xlabel('Est-Ouest')
        plt.ylabel('Nord-Sud')
        plt.savefig(soil_map_path)
        plt.close()
        
        # Obtenir des recommandations IA mockées
        ai_recommendations = self.ai_client.analyze_soil_quality(
            location, 
            crop_type,
            parameters or {}
        )
        
        # Propriétés du sol mockées
        soil_properties = {
            "texture": "limoneux-sableux",
            "ph": 6.5,
            "organic_matter": 2.8,
            "drainage": "bon",
            "depth": "profond (>60cm)",
            "water_retention": "moyenne"
        }
        
        # Résultats mockés
        return {
            "location": location,
            "crop_type": crop_type,
            "analysis_results": {
                "soil_properties": soil_properties,
                "compatibility": {
                    "ph_score": 8.5,
                    "drainage_score": 9.0,
                    "texture_score": 8.0,
                    "organic_score": 7.6,
                    "global_score": 8.3
                },
                "zones": zones
            },
            "ai_recommendations": ai_recommendations,
            "visualizations": {
                "map": map_path,
                "soil_map": soil_map_path
            }
        }
