"""
Service pour l'analyse d'emplacements commerciaux.
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
from src.models.commercial_location import CommercialLocation
from src.models.analysis_result import AnalysisResult

class CommercialLocationService:
    """
    Service pour l'analyse d'emplacements commerciaux.
    """
    def __init__(self, use_mock: bool = True):
        """
        Initialise le service d'analyse d'emplacements commerciaux.
        
        Args:
            use_mock (bool): Si True, utilise des données simulées au lieu de données réelles.
        """
        self.use_mock = use_mock
        self.deepseek_client = DeepseekClient(use_mock=use_mock)
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "src", "static", "visualizations")
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def analyze_location(self, location: CommercialLocation) -> AnalysisResult:
        """
        Analyse un emplacement commercial.
        
        Args:
            location (CommercialLocation): Emplacement à analyser
            
        Returns:
            AnalysisResult: Résultats de l'analyse
        """
        # Créer un résultat d'analyse
        result = AnalysisResult(analysis_type="commercial")
        
        try:
            # Récupérer les données géographiques
            if not self.use_mock:
                geo_data = self._get_geographic_data(location)
            else:
                geo_data = self._mock_geographic_data(location)
            
            # Analyser les données avec DeepSeek R1
            ai_analysis = self.deepseek_client.analyze_commercial_location(
                location.location_name,
                location.business_type,
                {
                    "radius": location.radius,
                    "importance_factors": location.importance_factors
                }
            )
            
            # Générer les visualisations
            visualizations = self._generate_visualizations(location, geo_data, ai_analysis)
            
            # Structurer les résultats
            result.scores = ai_analysis.get("analysis_results", {}).get("score", {})
            result.recommendations = ai_analysis.get("ai_recommendations", {}).get("recommendations", [])
            result.visualizations = visualizations
            result.raw_data = {
                "geo_data": geo_data,
                "ai_analysis": ai_analysis
            }
            
            # Mettre à jour les résultats dans l'objet location
            location.set_results({
                "score": result.scores,
                "recommendations": result.recommendations,
                "visualizations": result.visualizations
            })
            
            return result
            
        except Exception as e:
            print(f"Erreur lors de l'analyse de l'emplacement: {e}")
            result.add_score("error", 1.0)
            result.add_recommendation(f"Une erreur est survenue lors de l'analyse: {str(e)}")
            return result
    
    def _get_geographic_data(self, location: CommercialLocation) -> Dict[str, Any]:
        """
        Récupère les données géographiques pour un emplacement.
        
        Args:
            location (CommercialLocation): Emplacement à analyser
            
        Returns:
            dict: Données géographiques
        """
        # Récupérer les coordonnées géographiques si elles ne sont pas déjà définies
        if location.latitude == 0.0 and location.longitude == 0.0:
            try:
                gdf = ox.geocode_to_gdf(location.location_name)
                location.latitude = gdf.iloc[0].geometry.centroid.y
                location.longitude = gdf.iloc[0].geometry.centroid.x
            except Exception as e:
                print(f"Erreur lors de la géolocalisation: {e}")
                # Valeurs par défaut pour Paris
                location.latitude = 48.8566
                location.longitude = 2.3522
        
        # Créer un point pour l'emplacement
        point = Point(location.longitude, location.latitude)
        
        # Récupérer les données OpenStreetMap dans le rayon spécifié
        try:
            # Récupérer le réseau routier
            G = ox.graph_from_point((location.latitude, location.longitude), 
                                   dist=location.radius, 
                                   network_type='all')
            
            # Récupérer les points d'intérêt
            tags = {
                'amenity': True,
                'shop': True,
                'healthcare': True,
                'building': True
            }
            pois = ox.geometries_from_point((location.latitude, location.longitude), 
                                           tags=tags, 
                                           dist=location.radius)
            
            # Filtrer les concurrents en fonction du type de commerce
            competitors = self._filter_competitors(pois, location.business_type)
            
            # Calculer la densité du réseau routier
            road_density = len(G.edges) / (np.pi * (location.radius / 1000) ** 2)  # edges par km²
            
            return {
                "location": {
                    "name": location.location_name,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "radius": location.radius
                },
                "road_network": G,
                "pois": pois,
                "competitors": competitors,
                "road_density": road_density
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération des données géographiques: {e}")
            return {
                "location": {
                    "name": location.location_name,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "radius": location.radius
                },
                "error": str(e)
            }
    
    def _mock_geographic_data(self, location: CommercialLocation) -> Dict[str, Any]:
        """
        Génère des données géographiques simulées pour un emplacement.
        
        Args:
            location (CommercialLocation): Emplacement à analyser
            
        Returns:
            dict: Données géographiques simulées
        """
        # Si les coordonnées ne sont pas définies, utiliser des valeurs par défaut
        if location.latitude == 0.0 and location.longitude == 0.0:
            # Coordonnées par défaut en fonction du nom de l'emplacement
            if "paris" in location.location_name.lower():
                location.latitude = 48.8566
                location.longitude = 2.3522
            elif "lyon" in location.location_name.lower():
                location.latitude = 45.7578
                location.longitude = 4.8320
            elif "marseille" in location.location_name.lower():
                location.latitude = 43.2965
                location.longitude = 5.3698
            elif "toulouse" in location.location_name.lower():
                location.latitude = 43.6047
                location.longitude = 1.4442
            else:
                # Paris par défaut
                location.latitude = 48.8566
                location.longitude = 2.3522
        
        # Générer des POI simulés
        pois_count = {
            "pharmacy": 5,
            "hospital": 2,
            "school": 8,
            "supermarket": 6,
            "bus_stop": 15,
            "restaurant": 12,
            "bank": 4,
            "post_office": 1
        }
        
        # Générer des concurrents simulés en fonction du type de commerce
        competitors_count = 5
        if location.business_type.lower() == "pharmacie":
            competitors_name = "Pharmacie"
        elif location.business_type.lower() == "boulangerie":
            competitors_name = "Boulangerie"
            competitors_count = 8
        elif location.business_type.lower() == "supermarché":
            competitors_name = "Supermarché"
            competitors_count = 3
        else:
            competitors_name = location.business_type.capitalize()
        
        competitors = [
            {
                "name": f"{competitors_name} {chr(65+i)}",
                "distance": round(100 + i * 150 + np.random.randint(-50, 50), 0),
                "latitude": location.latitude + (np.random.random() - 0.5) * 0.01,
                "longitude": location.longitude + (np.random.random() - 0.5) * 0.01
            }
            for i in range(competitors_count)
        ]
        
        # Densité du réseau routier simulée
        road_density = 0.015  # edges par km²
        
        return {
            "location": {
                "name": location.location_name,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "radius": location.radius
            },
            "pois_count": pois_count,
            "competitors": competitors,
            "road_density": road_density
        }
    
    def _filter_competitors(self, pois: gpd.GeoDataFrame, business_type: str) -> List[Dict[str, Any]]:
        """
        Filtre les concurrents dans les points d'intérêt en fonction du type de commerce.
        
        Args:
            pois (GeoDataFrame): Points d'intérêt
            business_type (str): Type de commerce
            
        Returns:
            list: Liste des concurrents
        """
        competitors = []
        
        # Mapping des types de commerce vers les tags OSM
        business_type_mapping = {
            "pharmacie": {"amenity": "pharmacy"},
            "boulangerie": {"shop": "bakery"},
            "supermarché": {"shop": "supermarket"},
            "restaurant": {"amenity": "restaurant"},
            "café": {"amenity": "cafe"},
            "banque": {"amenity": "bank"},
            "école": {"amenity": "school"},
            "hôpital": {"amenity": "hospital"},
            "médecin": {"amenity": "doctors"},
            "dentiste": {"amenity": "dentist"}
        }
        
        # Récupérer les tags correspondant au type de commerce
        tags = business_type_mapping.get(business_type.lower(), {})
        
        if not tags:
            return competitors
        
        # Filtrer les POI en fonction des tags
        for tag_key, tag_value in tags.items():
            if tag_key in pois.columns:
                filtered_pois = pois[pois[tag_key] == tag_value]
                
                for _, poi in filtered_pois.iterrows():
                    name = poi.get("name", "Inconnu")
                    geometry = poi.geometry
                    
                    competitors.append({
                        "name": name,
                        "latitude": geometry.centroid.y,
                        "longitude": geometry.centroid.x
                    })
        
        return competitors
    
    def _generate_visualizations(self, 
                               location: CommercialLocation, 
                               geo_data: Dict[str, Any], 
                               ai_analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Génère les visualisations pour l'analyse d'emplacement commercial.
        
        Args:
            location (CommercialLocation): Emplacement analysé
            geo_data (dict): Données géographiques
            ai_analysis (dict): Analyse IA
            
        Returns:
            dict: Chemins vers les visualisations générées
        """
        visualizations = {}
        
        # Utiliser les visualisations simulées
        visualizations["map"] = "/static/visualizations/location_map.html"
        visualizations["heatmap"] = "/static/visualizations/location_heatmap.png"
        
        # Si on n'utilise pas les mocks, générer des visualisations réelles
        if not self.use_mock:
            try:
                # Générer une carte interactive
                map_path = self._generate_interactive_map(location, geo_data, ai_analysis)
                visualizations["map"] = map_path
                
                # Générer une heatmap
                heatmap_path = self._generate_heatmap(location, geo_data, ai_analysis)
                visualizations["heatmap"] = heatmap_path
            except Exception as e:
                print(f"Erreur lors de la génération des visualisations: {e}")
        
        return visualizations
    
    def _generate_interactive_map(self, 
                                location: CommercialLocation, 
                                geo_data: Dict[str, Any], 
                                ai_analysis: Dict[str, Any]) -> str:
        """
        Génère une carte interactive pour l'analyse d'emplacement commercial.
        
        Args:
            location (CommercialLocation): Emplacement analysé
            geo_data (dict): Données géographiques
            ai_analysis (dict): Analyse IA
            
        Returns:
            str: Chemin vers la carte générée
        """
        # Créer une carte Folium centrée sur l'emplacement
        m = folium.Map(
            location=[location.latitude, location.longitude],
            zoom_start=15,
            tiles="OpenStreetMap"
        )
        
        # Ajouter un cercle pour le rayon d'analyse
        folium.Circle(
            location=[location.latitude, location.longitude],
            radius=location.radius,
            color="#0d6efd",
            fill=True,
            fill_color="#0d6efd",
            fill_opacity=0.1
        ).add_to(m)
        
        # Ajouter les concurrents
        for competitor in geo_data.get("competitors", []):
            folium.CircleMarker(
                location=[competitor["latitude"], competitor["longitude"]],
                radius=5,
                color="#dc3545",
                fill=True,
                fill_color="#dc3545",
                fill_opacity=0.8,
                popup=competitor["name"]
            ).add_to(m)
        
        # Ajouter les hotspots (emplacements recommandés) s'ils existent
        hotspots = ai_analysis.get("ai_recommendations", {}).get("score", {})
        if hotspots:
            # Créer des points aléatoires autour de l'emplacement pour les hotspots
            for i, (name, score) in enumerate(hotspots.items()):
                # Générer des coordonnées aléatoires dans le rayon d'analyse
                angle = np.random.random() * 2 * np.pi
                distance = np.random.random() * location.radius * 0.8
                dx = distance * np.cos(angle) / 111320  # 1 degré = 111.32 km
                dy = distance * np.sin(angle) / (111320 * np.cos(location.latitude * np.pi / 180))
                
                lat = location.latitude + dy
                lon = location.longitude + dx
                
                # Déterminer la couleur en fonction du score
                if score > 8:
                    color = "#1a9641"
                elif score > 7:
                    color = "#a6d96a"
                elif score > 6:
                    color = "#ffffbf"
                else:
                    color = "#d7191c"
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=10,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.8,
                    popup=f"{name}: {score}/10"
                ).add_to(m)
        
        # Enregistrer la carte
        map_path = os.path.join(self.cache_dir, f"location_map_{location.location_id}.html")
        m.save(map_path)
        
        # Retourner le chemin relatif
        return f"/static/visualizations/location_map_{location.location_id}.html"
    
    def _generate_heatmap(self, 
                        location: CommercialLocation, 
                        geo_data: Dict[str, Any], 
                        ai_analysis: Dict[str, Any]) -> str:
        """
        Génère une heatmap pour l'analyse d'emplacement commercial.
        
        Args:
            location (CommercialLocation): Emplacement analysé
            geo_data (dict): Données géographiques
            ai_analysis (dict): Analyse IA
            
        Returns:
            str: Chemin vers la heatmap générée
        """
        # Créer une figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Générer une grille de points
        grid_size = 100
        x = np.linspace(location.longitude - 0.01, location.longitude + 0.01, grid_size)
        y = np.linspace(location.latitude - 0.01, location.latitude + 0.01, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Générer des valeurs d'attractivité simulées
        Z = np.zeros((grid_size, grid_size))
        
        # Ajouter un point chaud au centre
        center_x = grid_size // 2
        center_y = grid_size // 2
        for i in range(grid_size):
            for j in range(grid_size):
                # Distance au centre
                d = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                # Valeur d'attractivité décroissante avec la distance
                Z[i, j] = np.exp(-d / 20)
        
        # Ajouter des points chauds aléatoires
        for _ in range(5):
            x_idx = np.random.randint(0, grid_size)
            y_idx = np.random.randint(0, grid_size)
            intensity = np.random.random() * 0.8 + 0.2
            
            for i in range(grid_size):
                for j in range(grid_size):
                    # Distance au point chaud
                    d = np.sqrt((i - x_idx) ** 2 + (j - y_idx) ** 2)
                    # Valeur d'attractivité décroissante avec la distance
                    Z[i, j] += intensity * np.exp(-d / 15)
        
        # Normaliser les valeurs
        Z = Z / np.max(Z)
        
        # Créer la heatmap
        im = ax.imshow(Z, cmap='hot', extent=[x.min(), x.max(), y.min(), y.max()], 
                      origin='lower', alpha=0.7)
        
        # Ajouter une barre de couleur
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Attractivité')
        
        # Ajouter un titre
        plt.title(f"Carte de chaleur d'attractivité - {location.location_name}")
        
        # Enregistrer la figure
        heatmap_path = os.path.join(self.cache_dir, f"location_heatmap_{location.location_id}.png")
        plt.savefig(heatmap_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Retourner le chemin relatif
        return f"/static/visualizations/location_heatmap_{location.location_id}.png"
