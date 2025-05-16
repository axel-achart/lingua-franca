document.getElementById('translateBtn').addEventListener('click', () => {
  const sourceLang = document.getElementById('sourceLang').value;
  const targetLang = document.getElementById('targetLang').value;
  const sourceText = document.getElementById('sourceText').value.trim();

  if (!sourceText) {
    alert("Veuillez entrer du texte à traduire.");
    return;
  }

  fetch('/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: sourceText,
      source_lang: sourceLang,
      target_lang: targetLang
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('translatedText').value = data.translated_text || '❌ Traduction échouée';
  })
  .catch(error => {
    console.error('Erreur :', error);
    alert("Erreur de communication avec le serveur.");
  });
});
