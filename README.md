# 🌍 Lingua Franca Translate

**Lingua Franca** est une application web de traduction multilingue rapide et intuitive, construite avec **Flask**, **JavaScript**, et une API gratuite non officielle de **Google Translate**.

---

## 🚀 Fonctionnalités

- ✅ Traduction instantanée entre plusieurs langues
- 🧠 Détection automatique de la langue source
- 🔄 Bouton pour inverser les langues et les textes
- 💡 Interface responsive et facile à utiliser
- 🌐 API sans clé (Google Translate – Chrome client)

---

## 📸 Aperçu

![screenshot](static/screen_translator.jpg) <!-- À remplacer par une capture d'écran réelle -->

---

## 🛠️ Technologies utilisées

- Python 3
- Flask
- HTML5, CSS3, JavaScript
- API publique Google Translate (non officielle)

---

## 📂 Structure du projet

lingua-franca/
├── app.py # Backend Flask
├── requirements.txt # Dépendances Python
├── .gitignore # Fichiers à ignorer par Git
├── static/
│ ├── style.css # Feuille de style
│ ├── script.js # Code JS client
│ └── logo.jpg # Logo (optionnel)
├── templates/
│ └── index.html # Page principale


---

## ⚙️ Installation locale

1. **Clone le projet**

git clone https://github.com/tonprofil/lingua-franca.git

cd lingua-franca

python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

python app.py  

Va sur :
http://127.0.0.1:5000

📥 API utilisée
URL : https://clients5.google.com/translate_a/t
Utilisée par le client Chrome pour Google Translate.
⚠️ Cette API est non officielle : elle peut cesser de fonctionner si Google la restreint.

👨‍💻 Auteurs
Axel 

Rayanne 

Kylliann 

📝 Licence
Ce projet est open-source, à but éducatif uniquement.
Utilisation commerciale interdite si API non officielle utilisée.



