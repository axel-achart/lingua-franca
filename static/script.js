async function translateText() {
    const text = document.getElementById("inputText").value;
    const sl = document.getElementById("sourceLang").value;
    const tl = document.getElementById("targetLang").value;
    const output = document.getElementById("outputText");
    const button = document.getElementById("translateBtn");

    if (!text.trim()) {
        output.value = "";
        return;
    }

    button.disabled = true;
    button.textContent = "Traduction...";

    try {
        const res = await fetch("/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, sl, tl })
        });

        if (!res.ok) throw new Error("Erreur HTTP");

        const data = await res.json();
        output.value = data.translation || data.error || "❌ Traduction échouée";
    } catch (err) {
        output.value = "❌ Erreur de communication avec le serveur.";
        console.error("Erreur:", err);
    } finally {
        button.disabled = false;
        button.textContent = "Traduire";
    }
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
    outputTextarea.value = tempText;
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("swapLangButton")?.addEventListener("click", swapLanguages);
    document.getElementById("translateBtn")?.addEventListener("click", translateText);
});
