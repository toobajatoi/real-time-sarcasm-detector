document.addEventListener("DOMContentLoaded", () => {
  const meter = document.getElementById('meter');
  const socket = io();

  socket.on('sarcasm_update', data => {
    const pct = parseFloat(data.score).toFixed(2);
    meter.textContent = `Sarcasm Level: ${pct}%`;
    
    // Add visual feedback based on sarcasm level
    const score = data.score;
    let color;
    if (score < 30) {
      color = '#4CAF50';  // Green for low sarcasm
    } else if (score < 70) {
      color = '#FFC107';  // Yellow for medium sarcasm
    } else {
      color = '#F44336';  // Red for high sarcasm
    }
    meter.style.backgroundColor = color;
    meter.style.color = 'white';
  });
}); 