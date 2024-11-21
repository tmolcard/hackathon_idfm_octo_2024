import os
import urllib.parse

import requests
import pandas as pd

PRIM_API_TOKEN = os.environ['PRIM_API_TOKEN']
HEADERS = {'Accept': 'application/json', 'apikey': PRIM_API_TOKEN}

API_BASE_URL_PLACES = 'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/places?'
API_BASE_URL_JOURNEY = 'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/journeys?'


def process_dico(response: dict) -> dict:
    dicomax = {}

    itineraire = response['journeys'][0][0]

    etapes = {}

    for idx, step in enumerate(itineraire["sections"]):
        try:
            etapes[idx] = {
                "durée": step["duration"],
                "arrivée": step["to"]["name"],
                "départ": step["from"]["name"],
                "chemin": {}
            }
        except:
            continue
        if "path" in step:
            for idx2, _ in enumerate(step["path"]):
                etapes[idx]["chemin"][idx2] = step["path"][idx2]["instruction"]
            etapes[idx]["mode de mobilité"] = "marche"
        elif step.get("mode") != "walking":
            try:
                etapes[idx]["chemin"]["direction"] = step["display_informations"]["direction"]
                etapes[idx]["mode de mobilité"] = step["display_informations"]["commercial_mode"] + " " + step["display_informations"]["label"]
            except:
                continue
    dicomax[f'Itineraire {itineraire['type']}'] = {
        "duration": itineraire["duration"],
        "nombre changement": itineraire["nb_transfers"],
        "heure de départ": itineraire["departure_date_time"],
        "heure d'arrivée": itineraire["arrival_date_time"],
        "heure demandée": itineraire["requested_date_time"],
        "distance marche": itineraire["distances"]["walking"],
        "prix du trajet": itineraire["fare"],
        "étapes": etapes,

    }

    return dicomax


def get_place(adresse: str) -> str:
    params = {'q': adresse}
    url = API_BASE_URL_PLACES + urllib.parse.urlencode(params)

    # Envoi de la requête au serveur
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise ValueError(f"Error code {response.status_code}: {response.text}")
    response_dict = response.json()
    return response_dict["places"][0]["id"]


def call_riti(origin: str, destination: str, jour: str):
    # URL de l'API
    params = {
        'from': get_place(origin),
        'to': get_place(destination),
        'datetime': jour,
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

    response = call_riti(origin=origin, destination=destination, jour=jour)
    # process_dico(response)
