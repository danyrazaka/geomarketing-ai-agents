// Script principal pour GeoMarketing AI
document.addEventListener('DOMContentLoaded', function() {
  console.log('GeoMarketing AI - Application chargée');
  
  // Gestion des facteurs d'importance
  const factorRanges = document.querySelectorAll('.factor-range');
  if (factorRanges) {
    factorRanges.forEach(range => {
      const valueDisplay = range.nextElementSibling;
      range.addEventListener('input', () => {
        valueDisplay.textContent = range.value;
      });
    });
  }
  
  // Gestion du rayon d'analyse
  const radiusRange = document.getElementById('radius');
  if (radiusRange) {
    const radiusValue = document.getElementById('radius-value');
    radiusRange.addEventListener('input', () => {
      radiusValue.textContent = `${radiusRange.value}m`;
    });
  }
  
  // Gestion de la profondeur d'analyse
  const depthRange = document.getElementById('depth');
  if (depthRange) {
    const depthValue = document.getElementById('depth-value');
    depthRange.addEventListener('input', () => {
      depthValue.textContent = `${depthRange.value}cm`;
    });
  }
});
