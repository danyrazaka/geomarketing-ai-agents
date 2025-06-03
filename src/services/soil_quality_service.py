"""
Service pour l'analyse de la qualité des sols.
"""
import os
import json
import geopandas as gpd
import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple
import osmnx as ox
from shapely.geometry import Point, Polygon
import numpy as np
from src.utils.deepseek_client import DeepseekClient
from src.models.soil_quality import SoilQuality
from src.models.analysis_result import AnalysisResult

class SoilQualityService:
    """
    Service pour l'analyse de la qualité des sols.
    """
    def __init__(self, use_mock: bool = True):
        """
        Initialise le service d'analyse de la qualité des sols.
        
        Args:
            use_mock (bool): Si True, utilise des données simulées au lieu de données réelles.
        """
        self.use_mock = use_mock
        self.deepseek_client = DeepseekClient(use_mock=use_mock)
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "src", "static", "visualizations")
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def analyze_soil(self, soil: SoilQuality) -> AnalysisResult:
        """
        Analyse la qualité des sols.
        
        Args:
            soil (SoilQuality): Sol à analyser
            
        Returns:
            AnalysisResult: Résultats de l'analyse
        """
        # Créer un résultat d'analyse
        result = AnalysisResult(analysis_type="soil")
        
        try:
            # Récupérer les données pédologiques
            if not self.use_mock:
                soil_data = self._get_soil_data(soil)
            else:
                soil_data = self._mock_soil_data(soil)
            
            # Analyser les données avec DeepSeek R1
            ai_analysis = self.deepseek_client.analyze_soil_quality(
                soil.location_name,
                soil.crop_type,
                {
                    "depth": soil.depth,
                    "importance_factors": soil.importance_factors
                }
            )
            
            # Générer les visualisations
            visualizations = self._generate_visualizations(soil, soil_data, ai_analysis)
            
            # Structurer les résultats
            result.scores = ai_analysis.get("analysis_results", {}).get("compatibility", {})
            result.recommendations = ai_analysis.get("ai_recommendations", {}).get("recommendations", [])
            result.visualizations = visualizations
            result.raw_data = {
                "soil_data": soil_data,
                "ai_analysis": ai_analysis
            }
            
            # Mettre à jour les résultats dans l'objet soil
            soil.set_results({
                "compatibility": result.scores,
                "recommendations": result.recommendations,
                "visualizations": result.visualizations
            })
            
            return result
            
        except Exception as e:
            print(f"Erreur lors de l'analyse du sol: {e}")
            result.add_score("error", 1.0)
            result.add_recommendation(f"Une erreur est survenue lors de l'analyse: {str(e)}")
            return result
    
    def _get_soil_data(self, soil: SoilQuality) -> Dict[str, Any]:
        """
        Récupère les données pédologiques pour un sol.
        
        Args:
            soil (SoilQuality): Sol à analyser
            
        Returns:
            dict: Données pédologiques
        """
        # Récupérer les coordonnées géographiques si elles ne sont pas déjà définies
        if soil.latitude == 0.0 and soil.longitude == 0.0:
            try:
                gdf = ox.geocode_to_gdf(soil.location_name)
                soil.latitude = gdf.iloc[0].geometry.centroid.y
                soil.longitude = gdf.iloc[0].geometry.centroid.x
            except Exception as e:
                print(f"Erreur lors de la géolocalisation: {e}")
                # Valeurs par défaut pour Toulouse
                soil.latitude = 43.6047
                soil.longitude = 1.4442
        
        # Créer un point pour l'emplacement
        point = Point(soil.longitude, soil.latitude)
        
        # Récupérer les données de sol
        # Note: Dans une implémentation réelle, il faudrait accéder à des bases de données
        # pédologiques comme celles de l'INRAE ou de la FAO
        try:
            # Simuler des données de sol pour l'instant
            # Dans une version réelle, on utiliserait des services web ou des fichiers GeoTIFF
            soil_properties = {
                "texture": "limoneux-sableux",
                "ph": 6.5,
                "organic_matter": 2.8,
                "drainage": "bon",
                "depth": "profond (>60cm)",
                "water_retention": "moyenne"
            }
            
            # Simuler des zones de qualité de sol
            zones = [
                {
                    "name": "Zone optimale",
                    "proportion": 40,
                    "score": 8.7,
                    "color": "#1a9641",
                    "polygon": self._generate_random_polygon(soil.latitude, soil.longitude, 0.005, 0.002)
                },
                {
                    "name": "Zone intermédiaire",
                    "proportion": 35,
                    "score": 6.5,
                    "color": "#a6d96a",
                    "polygon": self._generate_random_polygon(soil.latitude - 0.003, soil.longitude - 0.002, 0.004, 0.002)
                },
                {
                    "name": "Zone peu adaptée",
                    "proportion": 25,
                    "score": 4.2,
                    "color": "#d7191c",
                    "polygon": self._generate_random_polygon(soil.latitude - 0.006, soil.longitude - 0.004, 0.003, 0.002)
                }
            ]
            
            # Simuler des échantillons de sol
            samples = [
                {
                    "position": [soil.latitude + 0.002, soil.longitude + 0.001],
                    "ph": 6.5,
                    "texture": "limoneux-sableux",
                    "organic_matter": 2.8
                },
                {
                    "position": [soil.latitude - 0.002, soil.longitude - 0.001],
                    "ph": 6.0,
                    "texture": "argileux",
                    "organic_matter": 2.2
                },
                {
                    "position": [soil.latitude - 0.005, soil.longitude - 0.003],
                    "ph": 5.5,
                    "texture": "lourd et compacté",
                    "organic_matter": 1.8
                }
            ]
            
            return {
                "location": {
                    "name": soil.location_name,
                    "latitude": soil.latitude,
                    "longitude": soil.longitude
                },
                "crop_type": soil.crop_type,
                "soil_properties": soil_properties,
                "zones": zones,
                "samples": samples
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération des données pédologiques: {e}")
            return {
                "location": {
                    "name": soil.location_name,
                    "latitude": soil.latitude,
                    "longitude": soil.longitude
                },
                "crop_type": soil.crop_type,
                "error": str(e)
            }
    
    def _mock_soil_data(self, soil: SoilQuality) -> Dict[str, Any]:
        """
        Génère des données pédologiques simulées pour un sol.
        
        Args:
            soil (SoilQuality): Sol à analyser
            
        Returns:
            dict: Données pédologiques simulées
        """
        # Si les coordonnées ne sont pas définies, utiliser des valeurs par défaut
        if soil.latitude == 0.0 and soil.longitude == 0.0:
            # Coordonnées par défaut en fonction du nom de l'emplacement
            if "paris" in soil.location_name.lower():
                soil.latitude = 48.8566
                soil.longitude = 2.3522
            elif "lyon" in soil.location_name.lower():
                soil.latitude = 45.7578
                soil.longitude = 4.8320
            elif "marseille" in soil.location_name.lower():
                soil.latitude = 43.2965
                soil.longitude = 5.3698
            elif "toulouse" in soil.location_name.lower():
                soil.latitude = 43.6047
                soil.longitude = 1.4442
            else:
                # Toulouse par défaut
                soil.latitude = 43.6047
                soil.longitude = 1.4442
        
        # Générer des propriétés de sol simulées
        soil_properties = {
            "texture": "limoneux-sableux",
            "ph": 6.5,
            "organic_matter": 2.8,
            "drainage": "bon",
            "depth": "profond (>60cm)",
            "water_retention": "moyenne"
        }
        
        # Ajuster les propriétés en fonction du type de culture
        if soil.crop_type.lower() == "stevia":
            # La stevia préfère un sol légèrement acide
            soil_properties["ph"] = 6.2
        elif soil.crop_type.lower() == "blé":
            # Le blé préfère un sol neutre à légèrement alcalin
            soil_properties["ph"] = 7.0
            soil_properties["texture"] = "limoneux"
        elif soil.crop_type.lower() == "riz":
            # Le riz préfère un sol argileux avec bonne rétention d'eau
            soil_properties["texture"] = "argileux"
            soil_properties["water_retention"] = "élevée"
            soil_properties["drainage"] = "moyen"
        
        # Générer des zones de qualité de sol
        zones = [
            {
                "name": "Zone optimale",
                "proportion": 40,
                "score": 8.7,
                "color": "#1a9641",
                "polygon": self._generate_random_polygon(soil.latitude, soil.longitude, 0.005, 0.002)
            },
            {
                "name": "Zone intermédiaire",
                "proportion": 35,
                "score": 6.5,
                "color": "#a6d96a",
                "polygon": self._generate_random_polygon(soil.latitude - 0.003, soil.longitude - 0.002, 0.004, 0.002)
            },
            {
                "name": "Zone peu adaptée",
                "proportion": 25,
                "score": 4.2,
                "color": "#d7191c",
                "polygon": self._generate_random_polygon(soil.latitude - 0.006, soil.longitude - 0.004, 0.003, 0.002)
            }
        ]
        
        # Générer des échantillons de sol
        samples = [
            {
                "position": [soil.latitude + 0.002, soil.longitude + 0.001],
                "ph": 6.5,
                "texture": "limoneux-sableux",
                "organic_matter": 2.8
            },
            {
                "position": [soil.latitude - 0.002, soil.longitude - 0.001],
                "ph": 6.0,
                "texture": "argileux",
                "organic_matter": 2.2
            },
            {
                "position": [soil.latitude - 0.005, soil.longitude - 0.003],
                "ph": 5.5,
                "texture": "lourd et compacté",
                "organic_matter": 1.8
            }
        ]
        
        return {
            "location": {
                "name": soil.location_name,
                "latitude": soil.latitude,
                "longitude": soil.longitude
            },
            "crop_type": soil.crop_type,
            "soil_properties": soil_properties,
            "zones": zones,
            "samples": samples
        }
    
    def _generate_random_polygon(self, 
                               center_lat: float, 
                               center_lon: float, 
                               radius_lat: float, 
                               radius_lon: float) -> List[List[float]]:
        """
        Génère un polygone aléatoire autour d'un point central.
        
        Args:
            center_lat (float): Latitude du centre
            center_lon (float): Longitude du centre
            radius_lat (float): Rayon en latitude
            radius_lon (float): Rayon en longitude
            
        Returns:
            list: Liste de points [lat, lon] formant le polygone
        """
        # Nombre de points du polygone
        n_points = np.random.randint(5, 10)
        
        # Générer des angles aléatoires
        angles = np.sort(np.random.random(n_points) * 2 * np.pi)
        
        # Générer des rayons aléatoires
        radii_lat = np.random.random(n_points) * 0.5 + 0.5  # Entre 0.5 et 1.0
        radii_lon = np.random.random(n_points) * 0.5 + 0.5  # Entre 0.5 et 1.0
        
        # Générer les points du polygone
        polygon = []
        for i in range(n_points):
            lat = center_lat + radius_lat * radii_lat[i] * np.sin(angles[i])
            lon = center_lon + radius_lon * radii_lon[i] * np.cos(angles[i])
            polygon.append([lat, lon])
        
        return polygon
    
    def _generate_visualizations(self, 
                               soil: SoilQuality, 
                               soil_data: Dict[str, Any], 
                               ai_analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Génère les visualisations pour l'analyse de la qualité des sols.
        
        Args:
            soil (SoilQuality): Sol analysé
            soil_data (dict): Données pédologiques
            ai_analysis (dict): Analyse IA
            
        Returns:
            dict: Chemins vers les visualisations générées
        """
        visualizations = {}
        
        # Utiliser les visualisations simulées
        visualizations["map"] = "/static/visualizations/soil_map.html"
        visualizations["soil_map"] = "/static/visualizations/soil_quality_map.png"
        
        # Si on n'utilise pas les mocks, générer des visualisations réelles
        if not self.use_mock:
            try:
                # Générer une carte interactive
                map_path = self._generate_interactive_map(soil, soil_data, ai_analysis)
                visualizations["map"] = map_path
                
                # Générer une carte de qualité des sols
                soil_map_path = self._generate_soil_quality_map(soil, soil_data, ai_analysis)
                visualizations["soil_map"] = soil_map_path
            except Exception as e:
                print(f"Erreur lors de la génération des visualisations: {e}")
        
        return visualizations
    
    def _generate_interactive_map(self, 
                                soil: SoilQuality, 
                                soil_data: Dict[str, Any], 
                                ai_analysis: Dict[str, Any]) -> str:
        """
        Génère une carte interactive pour l'analyse de la qualité des sols.
        
        Args:
            soil (SoilQuality): Sol analysé
            soil_data (dict): Données pédologiques
            ai_analysis (dict): Analyse IA
            
        Returns:
            str: Chemin vers la carte générée
        """
        # Créer une carte Folium centrée sur l'emplacement
        m = folium.Map(
            location=[soil.latitude, soil.longitude],
            zoom_start=15,
            tiles="OpenStreetMap"
        )
        
        # Ajouter les zones de qualité des sols
        for zone in soil_data.get("zones", []):
            folium.Polygon(
                locations=zone["polygon"],
                color=zone["color"],
                fill=True,
                fill_color=zone["color"],
                fill_opacity=0.5,
                popup=f"{zone['name']} - Score: {zone['score']}/10 - {zone['proportion']}%"
            ).add_to(m)
        
        # Ajouter les échantillons de sol
        for sample in soil_data.get("samples", []):
            folium.CircleMarker(
                location=sample["position"],
                radius=5,
                color="#000",
                fill=True,
                fill_color="#fff",
                fill_opacity=0.8,
                popup=f"pH: {sample['ph']}<br>Texture: {sample['texture']}<br>Matière organique: {sample['organic_matter']}%"
            ).add_to(m)
        
        # Ajouter une légende
        legend_html = """
        <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <h4>Légende</h4>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="background-color: #1a9641; width: 20px; height: 20px; margin-right: 8px;"></div>
                <div>Zone optimale</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="background-color: #a6d96a; width: 20px; height: 20px; margin-right: 8px;"></div>
                <div>Zone favorable</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="background-color: #ffffbf; width: 20px; height: 20px; margin-right: 8px;"></div>
                <div>Zone moyenne</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="background-color: #d7191c; width: 20px; height: 20px; margin-right: 8px;"></div>
                <div>Zone peu adaptée</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="background-color: #000; width: 20px; height: 20px; border-radius: 50%; margin-right: 8px;"></div>
                <div>Échantillon de sol</div>
            </div>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Enregistrer la carte
        map_path = os.path.join(self.cache_dir, f"soil_map_{soil.soil_id}.html")
        m.save(map_path)
        
        # Retourner le chemin relatif
        return f"/static/visualizations/soil_map_{soil.soil_id}.html"
    
    def _generate_soil_quality_map(self, 
                                 soil: SoilQuality, 
                                 soil_data: Dict[str, Any], 
                                 ai_analysis: Dict[str, Any]) -> str:
        """
        Génère une carte de qualité des sols.
        
        Args:
            soil (SoilQuality): Sol analysé
            soil_data (dict): Données pédologiques
            ai_analysis (dict): Analyse IA
            
        Returns:
            str: Chemin vers la carte générée
        """
        # Créer une figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Dessiner un fond blanc
        ax.set_facecolor('white')
        
        # Dessiner une grille légère
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Dessiner les zones de qualité des sols
        for zone in soil_data.get("zones", []):
            polygon = np.array(zone["polygon"])
            ax.fill(polygon[:, 1], polygon[:, 0], color=zone["color"], alpha=0.5, 
                   label=f"{zone['name']} ({zone['proportion']}%)")
            ax.plot(polygon[:, 1], polygon[:, 0], color='black', linewidth=1)
        
        # Dessiner les échantillons de sol
        for sample in soil_data.get("samples", []):
            ax.plot(sample["position"][1], sample["position"][0], 'ko', markersize=8, 
                   markerfacecolor='white', label='_nolegend_')
        
        # Ajouter une légende
        ax.legend(loc='upper right')
        
        # Ajouter un titre
        plt.title(f"Analyse de la qualité des sols pour {soil.crop_type} - {soil.location_name}")
        
        # Ajouter des étiquettes d'axes
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        
        # Enregistrer la figure
        soil_map_path = os.path.join(self.cache_dir, f"soil_quality_map_{soil.soil_id}.png")
        plt.savefig(soil_map_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Retourner le chemin relatif
        return f"/static/visualizations/soil_quality_map_{soil.soil_id}.png"
