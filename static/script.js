async function translateText() {
    const text = document.getElementById("inputText").value;
    const sl = document.getElementById("sourceLang").value;
    const tl = document.getElementById("targetLang").value;

    const res = await fetch("/translate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text, sl, tl })
    });

    const data = await res.json();
    document.getElementById("outputText").value = data.translation || data.error;
}

function swapLanguages() {
    const sourceLangSelect = document.getElementById("sourceLang");
    const targetLangSelect = document.getElementById("targetLang");
    const inputTextarea = document.getElementById("inputText");
    const outputTextarea = document.getElementById("outputText");

    // Swap language selections
    const tempLang = sourceLangSelect.value;
    sourceLangSelect.value = targetLangSelect.value;
    targetLangSelect.value = tempLang;

    // Swap text area contents
    const tempText = inputTextarea.value;
    inputTextarea.value = outputTextarea.value;
    outputTextarea.value = tempText; // Clear output or keep swapped text?
                                     // For now, keeping swapped text.
                                     // If output should be cleared, use: outputTextarea.value = "";
}

document.addEventListener('DOMContentLoaded', (event) => {
    const swapButton = document.getElementById("swapLangButton");
    if (swapButton) {
        swapButton.addEventListener("click", swapLanguages);
    }
});

function playTranslation() {
    const text = document.getElementById('outputText').value;
    const targetLang = document.getElementById('targetLang').value;

    if (!text) {
        alert("Any text to speak !");
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = targetLang;
    speechSynthesis.speak(utterance);
}
