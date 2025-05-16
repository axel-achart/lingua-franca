import requests

try:
    response = requests.post("https://libretranslate.de/translate", data={
        "q": "bonjour",
        "source": "fr",
        "target": "en",
        "format": "text"
    })
    print(response.status_code)
    print(response.text)
except Exception as e:
    print("Erreur de connexion :", e)
