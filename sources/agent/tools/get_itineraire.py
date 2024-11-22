from typing import Annotated

from langchain_core.tools import tool

from sources.api.api_prim import call_recherche_itineraire


@tool
def get_itineraire(
    origin: Annotated[
        str, "[Not null] Point de départ : une adresse ou une geolocation sous forme float;float."],
    destination: Annotated[
        str, "[Not null] Destination de l'itineraire recherché sous la forme d'une adresse."],
    jour: Annotated[
        str, "[Not null] Jour à laquelle l'utilisateur veut partir au format : YYYYmmdd"],
    heure: Annotated[
        str, "[Not null] Heure à laquelle l'utilisateur veut partir au format : HHMMSS"]
) -> str:
    """
        Récupère un itineraire permettant d'aller de origin à destination à une date donnée.
    """
    date_str = jour + "T" + heure
    return call_recherche_itineraire(origin=origin, destination=destination, date=date_str)
