import os
import urllib.parse

import requests
import pandas as pd

from sources.entities.process_dico import process_dico

PRIM_API_TOKEN = os.environ['PRIM_API_TOKEN']
HEADERS = {'Accept': 'application/json', 'apikey': PRIM_API_TOKEN}

API_BASE_URL_PLACES = 'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/places?'
API_BASE_URL_JOURNEY = 'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/journeys?'


def get_place(adresse: str) -> str:
    params = {'q': adresse}
    url = API_BASE_URL_PLACES + urllib.parse.urlencode(params)

    # Envoi de la requête au serveur
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise ValueError(f"Error code {response.status_code}: {response.text}")
    response_dict = response.json()
    return response_dict["places"][0]["id"]


def call_recherche_itineraire(origin: str, destination: str, date: str):
    # URL de l'API
    params = {
        'from': get_place(origin),
        'to': get_place(destination),
        'datetime': date,
    }

    url = API_BASE_URL_JOURNEY + urllib.parse.urlencode(params)

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise ValueError(f"Error code {response.status_code}: {response.text}")
    response = pd.json_normalize(response.json())
    return process_dico(response)


if __name__ == "__main__":
    # origin / destination
    origin = "14 rue du Prévôt, 75004 Paris"
    destination = "Censier-Daubenton"

    # Date et heure du trajet
    jour = "20241121T073000"

    response = call_recherche_itineraire(origin=origin, destination=destination, jour=jour)
