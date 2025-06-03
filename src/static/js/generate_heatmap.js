/* Carte de chaleur simulée pour l'analyse d'emplacement commercial */
/* Cette image est générée avec Canvas pour simuler une heatmap */

const canvas = document.createElement('canvas');
canvas.width = 800;
canvas.height = 600;
const ctx = canvas.getContext('2d');

// Fond blanc
ctx.fillStyle = 'white';
ctx.fillRect(0, 0, canvas.width, canvas.height);

// Dessiner une grille légère
ctx.strokeStyle = '#f0f0f0';
ctx.lineWidth = 1;
for (let i = 0; i < canvas.width; i += 50) {
  ctx.beginPath();
  ctx.moveTo(i, 0);
  ctx.lineTo(i, canvas.height);
  ctx.stroke();
}
for (let i = 0; i < canvas.height; i += 50) {
  ctx.beginPath();
  ctx.moveTo(0, i);
  ctx.lineTo(canvas.width, i);
  ctx.stroke();
}

// Créer un dégradé pour la heatmap
const gradient = ctx.createRadialGradient(400, 300, 10, 400, 300, 300);
gradient.addColorStop(0, 'rgba(255, 0, 0, 0.8)');
gradient.addColorStop(0.2, 'rgba(255, 255, 0, 0.6)');
gradient.addColorStop(0.4, 'rgba(0, 255, 0, 0.4)');
gradient.addColorStop(0.6, 'rgba(0, 0, 255, 0.2)');
gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

// Points chauds simulés
const hotspots = [
  { x: 400, y: 300, intensity: 1.0 },
  { x: 300, y: 350, intensity: 0.8 },
  { x: 500, y: 250, intensity: 0.7 },
  { x: 200, y: 200, intensity: 0.5 },
  { x: 600, y: 400, intensity: 0.6 }
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
ctx.fillText('Carte de chaleur d\'attractivité - Paris', 250, 30);

// Convertir en image
const dataURL = canvas.toDataURL('image/png');
