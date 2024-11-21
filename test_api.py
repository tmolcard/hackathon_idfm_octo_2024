import os

import requests
import pandas as pd

API_BASE_URL = 'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/journeys?from='
PRIM_API_TOKEN = os.environ['PRIM_API_TOKEN']


def call_api(dlong: str, dlat: str, along: str, alat: str, jour: str):
    # URL de l'API
    destination = dlong + "%3B%20" + dlat + "&to=" + along + "%3B%20" + alat + "&datetime=" + jour
    url = API_BASE_URL + destination

    # Le header doit contenir la clé API : apikey, remplacer #VOTRE CLE API par votre clé API
    headers = {'Accept': 'application/json', 'apikey': PRIM_API_TOKEN}

    # Envoi de la requête au serveur
    req = requests.get(url, headers=headers)

    # Affichage du code réponse
    print('Status:', req)

    # Lecture du json
    return pd.json_normalize(req.json())


if __name__ == "__main__":
    # longitude / latitude
    dlong = "2.33792"
    dlat = "48.85827"
    along = "2.3588523"
    alat = "48.9271087"

    # Date et heure du trajet
    jour = "20241121T073000"

    response = call_api(dlong=dlong, dlat=dlat, along=along, alat=alat, jour=jour)
    print(response)
