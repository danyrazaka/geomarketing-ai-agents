"""
Service pour l'analyse d'emplacement commercial.
"""
import os
import json
import geopandas as gpd
import osmnx as ox
import folium
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List, Tuple
from src.utils.deepseek_client import DeepSeekClient

class CommercialLocationService:
    """
    Service pour analyser et recommander des emplacements commerciaux optimaux.
    """
    def __init__(self, use_mock: bool = True):
        """
        Initialise le service d'analyse d'emplacement commercial.
        
        Args:
            use_mock: Si True, utilise des données mockées pour le développement
        """
        self.use_mock = use_mock
        self.ai_client = DeepSeekClient(use_mock=use_mock)
        
    def analyze_location(self, location: str, business_type: str = "pharmacie", 
                         parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyse un emplacement pour déterminer son potentiel commercial.
        
        Args:
            location: Nom ou coordonnées de l'emplacement (ex: "Paris, France")
            business_type: Type de commerce (ex: "pharmacie")
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats de l'analyse avec recommandations et visualisations
        """
        if self.use_mock:
            return self._mock_analysis(location, business_type, parameters)
        
        # Récupération des données OSM
        try:
            # Récupérer les données géographiques
            gdf_area = self._get_area_data(location)
            
            # Analyser les données
            analysis_results = self._analyze_area_data(gdf_area, business_type, parameters)
            
            # Générer des visualisations
            map_path, heatmap_path = self._generate_visualizations(gdf_area, analysis_results)
            
            # Obtenir des recommandations IA
            ai_recommendations = self.ai_client.analyze_commercial_location(
                location, 
                parameters or {}
            )
            
            # Combiner les résultats
            return {
                "location": location,
                "business_type": business_type,
                "analysis_results": analysis_results,
                "ai_recommendations": ai_recommendations,
                "visualizations": {
                    "map": map_path,
                    "heatmap": heatmap_path
                }
            }
        except Exception as e:
            print(f"Error analyzing location: {e}")
            return self._mock_analysis(location, business_type, parameters)
    
    def _get_area_data(self, location: str) -> gpd.GeoDataFrame:
        """
        Récupère les données géographiques d'une zone.
        
        Args:
            location: Nom ou coordonnées de l'emplacement
            
        Returns:
            GeoDataFrame contenant les données de la zone
        """
        # Récupérer les limites de la zone
        area = ox.geocode_to_gdf(location)
        
        # Récupérer les points d'intérêt dans la zone
        tags = {
            'amenity': ['pharmacy', 'hospital', 'clinic', 'doctors', 'school', 'university'],
            'shop': ['convenience', 'supermarket'],
            'highway': ['bus_stop', 'traffic_signals']
        }
        pois = ox.features_from_place(location, tags)
        
        # Récupérer le réseau routier
        graph = ox.graph_from_place(location, network_type='all')
        streets = ox.graph_to_gdfs(graph, nodes=False)
        
        # Combiner les données
        return {
            'area': area,
            'pois': pois,
            'streets': streets
        }
    
    def _analyze_area_data(self, gdf_area: Dict[str, gpd.GeoDataFrame], 
                          business_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse les données géographiques pour évaluer le potentiel commercial.
        
        Args:
            gdf_area: Dictionnaire de GeoDataFrames contenant les données de la zone
            business_type: Type de commerce
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats de l'analyse
        """
        # Exemple d'analyse simple
        # Dans une implémentation réelle, cette fonction serait beaucoup plus complexe
        
        # Compter les points d'intérêt par type
        poi_counts = {}
        if 'pois' in gdf_area and not gdf_area['pois'].empty:
            for col in ['amenity', 'shop', 'highway']:
                if col in gdf_area['pois'].columns:
                    value_counts = gdf_area['pois'][col].value_counts().to_dict()
                    poi_counts.update(value_counts)
        
        # Calculer la densité du réseau routier
        road_density = 0
        if 'streets' in gdf_area and not gdf_area['streets'].empty:
            total_length = gdf_area['streets'].length.sum()
            if 'area' in gdf_area and not gdf_area['area'].empty:
                area_size = gdf_area['area'].area.sum()
                if area_size > 0:
                    road_density = total_length / area_size
        
        # Identifier les concurrents potentiels
        competitors = []
        if business_type.lower() == 'pharmacie' and 'pois' in gdf_area and not gdf_area['pois'].empty:
            if 'amenity' in gdf_area['pois'].columns:
                pharmacies = gdf_area['pois'][gdf_area['pois']['amenity'] == 'pharmacy']
                competitors = pharmacies.shape[0]
        
        return {
            'poi_counts': poi_counts,
            'road_density': road_density,
            'competitors': competitors,
            'score': self._calculate_score(poi_counts, road_density, competitors)
        }
    
    def _calculate_score(self, poi_counts: Dict[str, int], road_density: float, 
                        competitors: int) -> Dict[str, float]:
        """
        Calcule un score d'attractivité basé sur les données analysées.
        
        Args:
            poi_counts: Nombre de points d'intérêt par type
            road_density: Densité du réseau routier
            competitors: Nombre de concurrents
            
        Returns:
            Scores d'attractivité pour différents critères
        """
        # Exemple de calcul de score simple
        # Dans une implémentation réelle, cette fonction serait plus sophistiquée
        
        # Score pour les points d'intérêt
        poi_score = min(sum(poi_counts.values()) / 10, 10)
        
        # Score pour la densité routière (normalisé entre 0 et 10)
        road_score = min(road_density * 1000, 10)
        
        # Score pour la concurrence (inversement proportionnel au nombre de concurrents)
        competition_score = max(10 - competitors, 0)
        
        # Score global (moyenne pondérée)
        global_score = (poi_score * 0.4 + road_score * 0.3 + competition_score * 0.3)
        
        return {
            'poi_score': round(poi_score, 1),
            'road_score': round(road_score, 1),
            'competition_score': round(competition_score, 1),
            'global_score': round(global_score, 1)
        }
    
    def _generate_visualizations(self, gdf_area: Dict[str, gpd.GeoDataFrame], 
                               analysis_results: Dict[str, Any]) -> Tuple[str, str]:
        """
        Génère des visualisations pour les résultats de l'analyse.
        
        Args:
            gdf_area: Dictionnaire de GeoDataFrames contenant les données de la zone
            analysis_results: Résultats de l'analyse
            
        Returns:
            Chemins vers les fichiers de visualisation générés
        """
        # Créer un dossier pour les visualisations si nécessaire
        os.makedirs('src/static/visualizations', exist_ok=True)
        
        # Générer une carte interactive avec Folium
        map_path = 'src/static/visualizations/location_map.html'
        
        if 'area' in gdf_area and not gdf_area['area'].empty:
            # Obtenir le centroïde de la zone
            centroid = gdf_area['area'].unary_union.centroid
            map_center = [centroid.y, centroid.x]
            
            # Créer la carte
            m = folium.Map(location=map_center, zoom_start=14)
            
            # Ajouter les limites de la zone
            folium.GeoJson(
                gdf_area['area'],
                name='Area',
                style_function=lambda x: {'fillColor': '#ffff00', 'color': '#000000', 'fillOpacity': 0.1}
            ).add_to(m)
            
            # Ajouter les points d'intérêt
            if 'pois' in gdf_area and not gdf_area['pois'].empty:
                for idx, row in gdf_area['pois'].iterrows():
                    if row.geometry:
                        popup_text = f"Type: {row.get('amenity') or row.get('shop') or row.get('highway')}"
                        folium.Marker(
                            [row.geometry.y, row.geometry.x],
                            popup=popup_text,
                            icon=folium.Icon(color='blue', icon='info-sign')
                        ).add_to(m)
            
            # Sauvegarder la carte
            m.save(map_path)
        else:
            # Carte par défaut si les données sont manquantes
            m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
            m.save(map_path)
        
        # Générer une heatmap simple
        heatmap_path = 'src/static/visualizations/location_heatmap.png'
        
        plt.figure(figsize=(10, 8))
        plt.title('Attractivité commerciale')
        
        # Exemple simple de heatmap
        # Dans une implémentation réelle, cette visualisation serait basée sur des données réelles
        x = np.linspace(0, 10, 20)
        y = np.linspace(0, 10, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y) * 5 + 5
        
        plt.contourf(X, Y, Z, cmap='viridis')
        plt.colorbar(label='Score d\'attractivité')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig(heatmap_path)
        plt.close()
        
        return map_path, heatmap_path
    
    def _mock_analysis(self, location: str, business_type: str, 
                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère une analyse mockée pour le développement et les tests.
        
        Args:
            location: Nom ou coordonnées de l'emplacement
            business_type: Type de commerce
            parameters: Paramètres spécifiques pour l'analyse
            
        Returns:
            Résultats mockés de l'analyse
        """
        # Créer un dossier pour les visualisations si nécessaire
        os.makedirs('src/static/visualizations', exist_ok=True)
        
        # Générer une carte simple
        map_path = 'src/static/visualizations/location_map.html'
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
        folium.Marker([48.8566, 2.3522], popup=f"Centre de {location}").add_to(m)
        m.save(map_path)
        
        # Générer une heatmap simple
        heatmap_path = 'src/static/visualizations/location_heatmap.png'
        plt.figure(figsize=(10, 8))
        plt.title('Attractivité commerciale (Données simulées)')
        x = np.linspace(0, 10, 20)
        y = np.linspace(0, 10, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y) * 5 + 5
        plt.contourf(X, Y, Z, cmap='viridis')
        plt.colorbar(label='Score d\'attractivité')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig(heatmap_path)
        plt.close()
        
        # Obtenir des recommandations IA mockées
        ai_recommendations = self.ai_client.analyze_commercial_location(
            location, 
            parameters or {}
        )
        
        # Résultats mockés
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
                    "poi_score": 8.5,
                    "road_score": 7.2,
                    "competition_score": 5.0,
                    "global_score": 7.1
                }
            },
            "ai_recommendations": ai_recommendations,
            "visualizations": {
                "map": map_path,
                "heatmap": heatmap_path
            }
        }
