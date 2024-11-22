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
        except KeyError:
            continue
        if "path" in step:
            for idx2, _ in enumerate(step["path"]):
                etapes[idx]["chemin"][idx2] = step["path"][idx2]["instruction"]
            etapes[idx]["mode de mobilité"] = "marche"
        else:
            try:
                etapes[idx]["chemin"]["direction"] = step["display_informations"]["direction"]
                etapes[idx]["mode de mobilité"] = (
                    step["display_informations"]["commercial_mode"] + " " +
                    step["display_informations"]["label"])
            except KeyError:
                continue

    dicomax[f"Itineraire {itineraire['type']}"] = {
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
