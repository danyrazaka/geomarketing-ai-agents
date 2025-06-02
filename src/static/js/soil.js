// Script pour la page d'analyse de la qualité des sols
document.addEventListener('DOMContentLoaded', function() {
  console.log('Page d\'analyse de la qualité des sols chargée');
  
  // Éléments du DOM
  const form = document.getElementById('soil-form');
  const loadExampleBtn = document.getElementById('load-example');
  const initialExampleBtn = document.getElementById('initial-example-btn');
  const initialContainer = document.getElementById('initial-container');
  const loadingContainer = document.getElementById('loading-container');
  const resultsContainer = document.getElementById('results-container');
  
  // Gestion du formulaire
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      analyzeSoil();
    });
  }
  
  // Chargement d'un exemple
  if (loadExampleBtn) {
    loadExampleBtn.addEventListener('click', loadExample);
  }
  
  if (initialExampleBtn) {
    initialExampleBtn.addEventListener('click', loadExample);
  }
  
  // Fonction pour analyser un sol
  function analyzeSoil() {
    // Afficher le chargement
    initialContainer.style.display = 'none';
    loadingContainer.style.display = 'block';
    resultsContainer.style.display = 'none';
    
    // Récupérer les données du formulaire
    const location = document.getElementById('location').value;
    const cropType = document.getElementById('crop-type').value;
    const depth = document.getElementById('depth').value;
    
    // Récupérer les facteurs d'importance
    const phFactor = document.getElementById('ph-factor').value / 10;
    const drainageFactor = document.getElementById('drainage-factor').value / 10;
    const textureFactor = document.getElementById('texture-factor').value / 10;
    const organicFactor = document.getElementById('organic-factor').value / 10;
    
    // Préparer les données pour l'API
    const data = {
      location: location,
      crop_type: cropType,
      parameters: {
        depth: parseInt(depth),
        importance_factors: {
          ph: phFactor,
          drainage: drainageFactor,
          texture: textureFactor,
          organic_matter: organicFactor
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
    fetch('/api/soil/examples')
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
          document.getElementById('crop-type').value = example.crop_type;
          
          if (example.parameters) {
            if (example.parameters.depth) {
              const depthInput = document.getElementById('depth');
              depthInput.value = example.parameters.depth;
              document.getElementById('depth-value').textContent = `${example.parameters.depth}cm`;
            }
            
            if (example.parameters.importance_factors) {
              const factors = example.parameters.importance_factors;
              
              if (factors.ph !== undefined) {
                const input = document.getElementById('ph-factor');
                input.value = Math.round(factors.ph * 10);
                input.nextElementSibling.textContent = input.value;
              }
              
              if (factors.drainage !== undefined) {
                const input = document.getElementById('drainage-factor');
                input.value = Math.round(factors.drainage * 10);
                input.nextElementSibling.textContent = input.value;
              }
              
              if (factors.texture !== undefined) {
                const input = document.getElementById('texture-factor');
                input.value = Math.round(factors.texture * 10);
                input.nextElementSibling.textContent = input.value;
              }
              
              if (factors.organic_matter !== undefined) {
                const input = document.getElementById('organic-factor');
                input.value = Math.round(factors.organic_matter * 10);
                input.nextElementSibling.textContent = input.value;
              }
            }
          }
          
          // Lancer l'analyse avec les données de l'exemple
          analyzeSoil();
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
    document.getElementById('location').value = 'Toulouse, France';
    document.getElementById('crop-type').value = 'stevia';
    document.getElementById('depth').value = 30;
    document.getElementById('depth-value').textContent = '30cm';
    
    document.getElementById('ph-factor').value = 3;
    document.getElementById('ph-factor').nextElementSibling.textContent = '3';
    
    document.getElementById('drainage-factor').value = 3;
    document.getElementById('drainage-factor').nextElementSibling.textContent = '3';
    
    document.getElementById('texture-factor').value = 2;
    document.getElementById('texture-factor').nextElementSibling.textContent = '2';
    
    document.getElementById('organic-factor').value = 2;
    document.getElementById('organic-factor').nextElementSibling.textContent = '2';
    
    analyzeSoil();
  }
  
  // Fonction pour simuler une réponse de l'API
  function mockApiResponse(requestData) {
    // Simuler une réponse de l'API
    const response = {
      location: requestData.location,
      crop_type: requestData.crop_type,
      analysis_results: {
        soil_properties: {
          texture: "limoneux-sableux",
          ph: 6.5,
          organic_matter: 2.8,
          drainage: "bon",
          depth: "profond (>60cm)",
          water_retention: "moyenne"
        },
        compatibility: {
          ph_score: 8.5,
          drainage_score: 9.0,
          texture_score: 8.0,
          organic_score: 7.6,
          global_score: 8.3
        },
        zones: [
          {
            name: "Zone optimale",
            proportion: 40,
            score: 8.7,
            color: "green"
          },
          {
            name: "Zone intermédiaire",
            proportion: 35,
            score: 6.5,
            color: "yellow"
          },
          {
            name: "Zone peu adaptée",
            proportion: 25,
            score: 4.2,
            color: "red"
          }
        ]
      },
      ai_recommendations: {
        location: requestData.location,
        crop_type: requestData.crop_type,
        analysis: `Analyse de la qualité des sols pour ${requestData.location} concernant la culture de ${requestData.crop_type}:\n\nAprès analyse des données pédologiques, climatiques et hydrologiques, voici mes conclusions:\n\n1. Zone optimale: La partie sud-est de la parcelle (environ 40% de la surface totale) présente les meilleures conditions.\n   - Caractéristiques: Sol limoneux-sableux, pH 6.2-6.8 (légèrement acide, idéal pour la stevia), bonne capacité de drainage.\n   - Recommandations: Aucun amendement majeur nécessaire, système d'irrigation goutte-à-goutte recommandé.\n\n2. Zone intermédiaire: La partie centrale (environ 35% de la surface).\n   - Caractéristiques: Sol plus argileux, pH 5.8-6.2 (un peu trop acide), drainage moyen.\n   - Recommandations: Amendement calcaire léger (500kg/ha), amélioration du drainage par sous-solage.\n\n3. Zone peu adaptée: La partie nord-ouest (environ 25% de la surface).\n   - Caractéristiques: Sol lourd et compacté, pH 5.5 (trop acide), risque d'engorgement.\n   - Recommandations: Utiliser pour d'autres cultures ou réaliser des travaux importants (drainage, amendements organiques et calcaires).\n\nPour maximiser le rendement de stevia, je recommande de concentrer la culture sur les zones 1 et 2, avec les amendements appropriés pour la zone 2. La zone 3 pourrait être réservée à d'autres cultures moins sensibles aux conditions acides et à l'engorgement.`,
        zones: [
          {
            name: "Zone optimale",
            proportion: 40,
            characteristics: ["Sol limoneux-sableux", "pH 6.2-6.8", "Bonne capacité de drainage"],
            recommendations: ["Aucun amendement majeur nécessaire", "Système d'irrigation goutte-à-goutte recommandé"]
          },
          {
            name: "Zone intermédiaire",
            proportion: 35,
            characteristics: ["Sol plus argileux", "pH 5.8-6.2", "Drainage moyen"],
            recommendations: ["Amendement calcaire léger (500kg/ha)", "Amélioration du drainage par sous-solage"]
          },
          {
            name: "Zone peu adaptée",
            proportion: 25,
            characteristics: ["Sol lourd et compacté", "pH 5.5", "Risque d'engorgement"],
            recommendations: ["Utiliser pour d'autres cultures", "Ou réaliser des travaux importants (drainage, amendements)"]
          }
        ],
        recommendations: [
          "Pour maximiser le rendement de stevia, je recommande de concentrer la culture sur les zones 1 et 2, avec les amendements appropriés pour la zone 2.",
          "La zone 3 pourrait être réservée à d'autres cultures moins sensibles aux conditions acides et à l'engorgement."
        ]
      },
      visualizations: {
        map: "/static/visualizations/soil_map.html",
        soil_map: "/static/visualizations/soil_quality_map.png"
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
    
    // Mettre à jour le nom de la culture
    document.getElementById('crop-name').textContent = data.crop_type;
    
    // Afficher les scores
    if (data.analysis_results && data.analysis_results.compatibility) {
      const compatibility = data.analysis_results.compatibility;
      document.getElementById('global-score').textContent = compatibility.global_score;
      document.getElementById('ph-score').textContent = compatibility.ph_score;
      document.getElementById('drainage-score').textContent = compatibility.drainage_score;
      document.getElementById('texture-score').textContent = compatibility.texture_score;
    }
    
    // Afficher la carte
    const mapFrame = document.getElementById('map-frame');
    if (mapFrame && data.visualizations && data.visualizations.map) {
      mapFrame.src = data.visualizations.map;
    }
    
    // Afficher la carte de qualité des sols
    const soilMapImage = document.getElementById('soil-map-image');
    if (soilMapImage && data.visualizations && data.visualizations.soil_map) {
      soilMapImage.src = data.visualizations.soil_map;
      soilMapImage.alt = `Carte de qualité des sols pour ${data.location}`;
    }
    
    // Afficher les recommandations
    const aiRecommendations = document.getElementById('ai-recommendations');
    if (aiRecommendations && data.ai_recommendations) {
      aiRecommendations.innerHTML = data.ai_recommendations.analysis.replace(/\n/g, '<br>');
    }
    
    // Afficher les propriétés du sol
    if (data.analysis_results && data.analysis_results.soil_properties) {
      const properties = data.analysis_results.soil_properties;
      document.getElementById('soil-texture').textContent = properties.texture;
      document.getElementById('soil-ph').textContent = properties.ph;
      document.getElementById('soil-organic').textContent = `${properties.organic_matter}%`;
      document.getElementById('soil-drainage').textContent = properties.drainage;
    }
    
    // Afficher les zones
    const zonesSummary = document.getElementById('zones-summary');
    if (zonesSummary && data.analysis_results && data.analysis_results.zones) {
      zonesSummary.innerHTML = '';
      
      data.analysis_results.zones.forEach(zone => {
        const zoneCard = document.createElement('div');
        zoneCard.className = 'card mb-2';
        
        const cardHeader = document.createElement('div');
        cardHeader.className = `card-header ${zone.color === 'green' ? 'bg-success' : zone.color === 'yellow' ? 'bg-warning' : 'bg-danger'} text-white`;
        cardHeader.innerHTML = `${zone.name} (${zone.proportion}%)`;
        
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body py-2';
        cardBody.innerHTML = `<p class="mb-1"><strong>Score:</strong> ${zone.score}/10</p>`;
        
        zoneCard.appendChild(cardHeader);
        zoneCard.appendChild(cardBody);
        zonesSummary.appendChild(zoneCard);
      });
    }
  }
});
