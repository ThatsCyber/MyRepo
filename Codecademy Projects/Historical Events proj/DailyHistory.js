function showHistoricalFact() {
  const modal = document.getElementById('historicalFactModal');
  modal.style.display = "block";
  const currentDate = new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  const historicalFact = `On, ${currentDate}, something interesting happened!`; // Replace with actual logic to fetch facts
  document.getElementById('historical-fact').textContent = historicalFact;
}

function closeModal() {
  const modal = document.getElementById('historicalFactModal');
  modal.style.display = "none";
}

// Example logic to update the date (this can be replaced with actual date logic)
document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', {
  month: 'long',
  day: 'numeric',
  year: 'numeric'
});
