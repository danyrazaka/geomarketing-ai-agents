// Script pour la page d'analyse d'emplacement commercial
document.addEventListener('DOMContentLoaded', function() {
  console.log('Page d\'analyse d\'emplacement commercial chargée');
  
  // Éléments du DOM
  const form = document.getElementById('commercial-form');
  const loadExampleBtn = document.getElementById('load-example');
  const initialExampleBtn = document.getElementById('initial-example-btn');
  const initialContainer = document.getElementById('initial-container');
  const loadingContainer = document.getElementById('loading-container');
  const resultsContainer = document.getElementById('results-container');
  
  // Gestion du formulaire
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      analyzeLocation();
    });
  }
  
  // Chargement d'un exemple
  if (loadExampleBtn) {
    loadExampleBtn.addEventListener('click', loadExample);
  }
  
  if (initialExampleBtn) {
    initialExampleBtn.addEventListener('click', loadExample);
  }
  
  // Fonction pour analyser un emplacement
  function analyzeLocation() {
    // Afficher le chargement
    initialContainer.style.display = 'none';
    loadingContainer.style.display = 'block';
    resultsContainer.style.display = 'none';
    
    // Récupérer les données du formulaire
    const location = document.getElementById('location').value;
    const businessType = document.getElementById('business-type').value;
    const radius = document.getElementById('radius').value;
    
    // Récupérer les facteurs d'importance
    const populationFactor = document.getElementById('population-factor').value / 10;
    const competitionFactor = document.getElementById('competition-factor').value / 10;
    const accessibilityFactor = document.getElementById('accessibility-factor').value / 10;
    const visibilityFactor = document.getElementById('visibility-factor').value / 10;
    
    // Préparer les données pour l'API
    const data = {
      location: location,
      business_type: businessType,
      parameters: {
        radius: parseInt(radius),
        importance_factors: {
          population: populationFactor,
          competition: competitionFactor,
          accessibility: accessibilityFactor,
          visibility: visibilityFactor
        }
      }
    };
    
    // Appel à l'API (simulé pour le prototype)
    console.log('Données envoyées à l\'API:', data);
    
    // Simuler un délai de chargement
    setTimeout(() => {
      // Dans une implémentation réelle, ceci serait un appel fetch à l'API
      mockApiResponse(data);
    }, 2000);
  }
  
  // Fonction pour charger un exemple
  function loadExample() {
    // Simuler un appel à l'API pour récupérer un exemple
    fetch('/api/commercial/examples')
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de la récupération des exemples');
        }
        return response.json();
      })
      .then(examples => {
        if (examples && examples.length > 0) {
          const example = examples[0]; // Prendre le premier exemple
          
          // Remplir le formulaire avec les données de l'exemple
          document.getElementById('location').value = example.location;
          document.getElementById('business-type').value = example.business_type;
          
          if (example.parameters) {
            if (example.parameters.radius) {
              const radiusInput = document.getElementById('radius');
              radiusInput.value = example.parameters.radius;
              document.getElementById('radius-value').textContent = `${example.parameters.radius}m`;
            }
            
            if (example.parameters.importance_factors) {
              const factors = example.parameters.importance_factors;
              
              if (factors.population !== undefined) {
                const input = document.getElementById('population-factor');
                input.value = Math.round(factors.population * 10);
                input.nextElementSibling.textContent = input.value;
              }
              
              if (factors.competition !== undefined) {
                const input = document.getElementById('competition-factor');
                input.value = Math.round(factors.competition * 10);
                input.nextElementSibling.textContent = input.value;
              }
              
              if (factors.accessibility !== undefined) {
                const input = document.getElementById('accessibility-factor');
                input.value = Math.round(factors.accessibility * 10);
                input.nextElementSibling.textContent = input.value;
              }
            }
          }
          
          // Lancer l'analyse avec les données de l'exemple
          analyzeLocation();
        }
      })
      .catch(error => {
        console.error('Erreur:', error);
        // Utiliser des données mockées en cas d'erreur
        mockExample();
      });
  }
  
  // Fonction pour simuler un exemple en cas d'erreur
  function mockExample() {
    document.getElementById('location').value = 'Paris, France';
    document.getElementById('business-type').value = 'pharmacie';
    document.getElementById('radius').value = 500;
    document.getElementById('radius-value').textContent = '500m';
    
    document.getElementById('population-factor').value = 4;
    document.getElementById('population-factor').nextElementSibling.textContent = '4';
    
    document.getElementById('competition-factor').value = 3;
    document.getElementById('competition-factor').nextElementSibling.textContent = '3';
    
    document.getElementById('accessibility-factor').value = 3;
    document.getElementById('accessibility-factor').nextElementSibling.textContent = '3';
    
    document.getElementById('visibility-factor').value = 3;
    document.getElementById('visibility-factor').nextElementSibling.textContent = '3';
    
    analyzeLocation();
  }
  
  // Fonction pour simuler une réponse de l'API
  function mockApiResponse(requestData) {
    // Simuler une réponse de l'API
    const response = {
      location: requestData.location,
      business_type: requestData.business_type,
      analysis_results: {
        poi_counts: {
          pharmacy: 5,
          hospital: 2,
          school: 8,
          supermarket: 6,
          bus_stop: 15
        },
        road_density: 0.015,
        competitors: 5,
        score: {
          poi_score: 8.5,
          road_score: 7.2,
          competition_score: 5.0,
          global_score: 7.1
        }
      },
      ai_recommendations: {
        location: requestData.location,
        analysis: `Analyse d'emplacement commercial pour ${requestData.location}:\n\nAprès analyse des données démographiques, des flux de circulation et de la concurrence, voici mes recommandations:\n\n1. Emplacement optimal: Le secteur nord-est de la zone présente le meilleur potentiel avec un score d'attractivité de 8.7/10.\n   - Avantages: Forte densité de population (environ 5000 habitants dans un rayon de 500m), proximité d'un centre médical, bon accès aux transports en commun.\n   - Inconvénients: Présence d'un concurrent à 800m, stationnement limité.\n\n2. Emplacement alternatif: Le carrefour central avec un score d'attractivité de 7.9/10.\n   - Avantages: Excellente visibilité, fort passage piétonnier (environ 1200 personnes/heure), synergie avec commerces existants.\n   - Inconvénients: Loyer potentiellement plus élevé, concurrence plus forte.\n\n3. Emplacement de niche: La zone résidentielle sud avec un score de 7.2/10.\n   - Avantages: Faible concurrence, population vieillissante (bon marché pour une pharmacie), stationnement facile.\n   - Inconvénients: Moindre visibilité, accès limité en transports en commun.\n\nJe recommande de privilégier le premier emplacement qui offre le meilleur équilibre entre accessibilité, visibilité et potentiel commercial.`,
        recommendations: [
          "Je recommande de privilégier le premier emplacement qui offre le meilleur équilibre entre accessibilité, visibilité et potentiel commercial."
        ],
        score: {
          emplacement_1: 8.7,
          emplacement_2: 7.9,
          emplacement_3: 7.2
        }
      },
      visualizations: {
        map: "/static/visualizations/location_map.html",
        heatmap: "/static/visualizations/location_heatmap.png"
      }
    };
    
    // Afficher les résultats
    displayResults(response);
  }
  
  // Fonction pour afficher les résultats
  function displayResults(data) {
    // Masquer le chargement et afficher les résultats
    loadingContainer.style.display = 'none';
    resultsContainer.style.display = 'block';
    
    // Afficher les scores
    document.getElementById('global-score').textContent = data.analysis_results.score.global_score;
    document.getElementById('poi-score').textContent = data.analysis_results.score.poi_score;
    document.getElementById('road-score').textContent = data.analysis_results.score.road_score;
    document.getElementById('competition-score').textContent = data.analysis_results.score.competition_score;
    
    // Afficher la carte
    const mapFrame = document.getElementById('map-frame');
    if (mapFrame && data.visualizations && data.visualizations.map) {
      mapFrame.src = data.visualizations.map;
    }
    
    // Afficher la heatmap
    const heatmapImage = document.getElementById('heatmap-image');
    if (heatmapImage && data.visualizations && data.visualizations.heatmap) {
      heatmapImage.src = data.visualizations.heatmap;
      heatmapImage.alt = `Carte de chaleur d'attractivité pour ${data.location}`;
    }
    
    // Afficher les recommandations
    const aiRecommendations = document.getElementById('ai-recommendations');
    if (aiRecommendations && data.ai_recommendations) {
      aiRecommendations.innerHTML = data.ai_recommendations.analysis.replace(/\n/g, '<br>');
    }
    
    // Afficher les données d'analyse
    const poiTable = document.getElementById('poi-table');
    if (poiTable && data.analysis_results && data.analysis_results.poi_counts) {
      poiTable.innerHTML = '';
      for (const [type, count] of Object.entries(data.analysis_results.poi_counts)) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${type}</td><td>${count}</td>`;
        poiTable.appendChild(row);
      }
    }
    
    // Afficher les autres métriques
    if (data.analysis_results) {
      document.getElementById('road-density').textContent = data.analysis_results.road_density.toFixed(3);
      document.getElementById('competitors-count').textContent = data.analysis_results.competitors;
    }
  }
});
