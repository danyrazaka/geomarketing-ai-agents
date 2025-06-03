/* Génération d'images statiques pour les visualisations */
const fs = require('fs');
const { createCanvas } = require('canvas');

// Fonction pour générer une carte de chaleur
function generateHeatmap(width, height, filename, title, location) {
    const canvas = createCanvas(width, height);
    const ctx = canvas.getContext('2d');

    // Fond blanc
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);

    // Dessiner une grille légère
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    for (let i = 0; i < width; i += 50) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, height);
        ctx.stroke();
    }
    for (let i = 0; i < height; i += 50) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(width, i);
        ctx.stroke();
    }

    // Points chauds simulés
    const hotspots = [
        { x: width/2, y: height/2, intensity: 1.0 },
        { x: width/2 - 100, y: height/2 + 50, intensity: 0.8 },
        { x: width/2 + 100, y: height/2 - 50, intensity: 0.7 },
        { x: width/2 - 200, y: height/2 - 100, intensity: 0.5 },
        { x: width/2 + 200, y: height/2 + 100, intensity: 0.6 }
    ];

    // Dessiner les points chauds
    hotspots.forEach(spot => {
        ctx.globalAlpha = spot.intensity;
        const spotGradient = ctx.createRadialGradient(
            spot.x, spot.y, 10,
            spot.x, spot.y, 150
        );
        spotGradient.addColorStop(0, 'rgba(255, 0, 0, 0.8)');
        spotGradient.addColorStop(0.2, 'rgba(255, 255, 0, 0.6)');
        spotGradient.addColorStop(0.4, 'rgba(0, 255, 0, 0.4)');
        spotGradient.addColorStop(0.6, 'rgba(0, 0, 255, 0.2)');
        spotGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        
        ctx.fillStyle = spotGradient;
        ctx.beginPath();
        ctx.arc(spot.x, spot.y, 150, 0, Math.PI * 2);
        ctx.fill();
    });

    // Réinitialiser l'opacité
    ctx.globalAlpha = 1.0;

    // Ajouter une légende
    ctx.fillStyle = 'white';
    ctx.fillRect(20, 20, 200, 120);
    ctx.strokeStyle = '#333';
    ctx.strokeRect(20, 20, 200, 120);

    ctx.fillStyle = '#333';
    ctx.font = '14px Arial';
    ctx.fillText('Attractivité', 30, 40);

    const legendColors = [
        { color: 'rgb(255, 0, 0)', text: 'Très élevée' },
        { color: 'rgb(255, 255, 0)', text: 'Élevée' },
        { color: 'rgb(0, 255, 0)', text: 'Moyenne' },
        { color: 'rgb(0, 0, 255)', text: 'Faible' }
    ];

    legendColors.forEach((item, index) => {
        const y = 60 + index * 20;
        ctx.fillStyle = item.color;
        ctx.fillRect(30, y, 20, 10);
        ctx.fillStyle = '#333';
        ctx.fillText(item.text, 60, y + 10);
    });

    // Ajouter un titre
    ctx.fillStyle = '#333';
    ctx.font = 'bold 20px Arial';
    ctx.fillText(`${title} - ${location}`, width/2 - 150, 30);

    // Enregistrer l'image
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(filename, buffer);
    console.log(`Image générée: ${filename}`);
}

// Fonction pour générer une carte de qualité des sols
function generateSoilQualityMap(width, height, filename, location, cropType) {
    const canvas = createCanvas(width, height);
    const ctx = canvas.getContext('2d');

    // Fond blanc
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);

    // Dessiner une grille légère
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    for (let i = 0; i < width; i += 50) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, height);
        ctx.stroke();
    }
    for (let i = 0; i < height; i += 50) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(width, i);
        ctx.stroke();
    }

    // Zones de qualité des sols
    const zones = [
        { 
            name: "Zone optimale", 
            color: "#1a9641", 
            proportion: 40,
            polygon: [
                [width/2 + 80, height/2 - 120],
                [width/2 + 70, height/2 + 80],
                [width/2 - 30, height/2 + 70],
                [width/2 - 20, height/2 - 110]
            ]
        },
        { 
            name: "Zone intermédiaire", 
            color: "#a6d96a", 
            proportion: 35,
            polygon: [
                [width/2 - 20, height/2 - 110],
                [width/2 - 30, height/2 + 70],
                [width/2 - 100, height/2 + 60],
                [width/2 - 90, height/2 - 120]
            ]
        },
        { 
            name: "Zone peu adaptée", 
            color: "#d7191c", 
            proportion: 25,
            polygon: [
                [width/2 - 90, height/2 - 120],
                [width/2 - 100, height/2 + 60],
                [width/2 - 170, height/2 + 50],
                [width/2 - 160, height/2 - 130]
            ]
        }
    ];

    // Dessiner les zones
    zones.forEach(zone => {
        ctx.fillStyle = zone.color;
        ctx.beginPath();
        ctx.moveTo(zone.polygon[0][0], zone.polygon[0][1]);
        for (let i = 1; i < zone.polygon.length; i++) {
            ctx.lineTo(zone.polygon[i][0], zone.polygon[i][1]);
        }
        ctx.closePath();
        ctx.fill();
        
        // Ajouter un contour
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;
        ctx.stroke();
    });

    // Ajouter des points d'échantillonnage
    const samples = [
        { x: width/2 + 30, y: height/2 - 20 },
        { x: width/2 - 50, y: height/2 + 10 },
        { x: width/2 - 130, y: height/2 - 30 }
    ];

    samples.forEach(sample => {
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(sample.x, sample.y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.stroke();
    });

    // Ajouter une légende
    ctx.fillStyle = 'white';
    ctx.fillRect(20, 20, 220, 140);
    ctx.strokeStyle = '#333';
    ctx.strokeRect(20, 20, 220, 140);

    ctx.fillStyle = '#333';
    ctx.font = '14px Arial';
    ctx.fillText('Qualité des sols', 30, 40);

    zones.forEach((zone, index) => {
        const y = 60 + index * 20;
        ctx.fillStyle = zone.color;
        ctx.fillRect(30, y, 20, 10);
        ctx.fillStyle = '#333';
        ctx.fillText(`${zone.name} (${zone.proportion}%)`, 60, y + 10);
    });

    // Point d'échantillonnage dans la légende
    const y = 60 + zones.length * 20;
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(40, y + 5, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.fillStyle = '#333';
    ctx.fillText('Point d\'échantillonnage', 60, y + 10);

    // Ajouter un titre
    ctx.fillStyle = '#333';
    ctx.font = 'bold 20px Arial';
    ctx.fillText(`Analyse des sols pour ${cropType} - ${location}`, width/2 - 180, 30);

    // Enregistrer l'image
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(filename, buffer);
    console.log(`Image générée: ${filename}`);
}

// Générer les images
try {
    generateHeatmap(800, 600, 'location_heatmap.png', 'Carte de chaleur d\'attractivité', 'Paris');
    generateSoilQualityMap(800, 600, 'soil_quality_map.png', 'Toulouse', 'stevia');
    console.log('Génération des images terminée avec succès');
} catch (error) {
    console.error('Erreur lors de la génération des images:', error);
}
