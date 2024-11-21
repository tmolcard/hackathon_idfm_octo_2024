from sources.api.api_prim import call_recherche_itineraire


from langchain_core.tools import tool


from typing import Annotated


@tool
def get_itineraire(
    origin: Annotated[
        str, "Point de départ sous la forme d'une adresse."],
    destination: Annotated[
        str, "Destination de l'itineraire recherché sous la forme d'une adresse."],
    jour: Annotated[
        str, "Jour à laquelle l'utilisateur veut partir au format : YYYYmmdd"],
    heure: Annotated[
        str, "Heure à laquelle l'utilisateur veut partir au format : HHMMSS"]
) -> str:
    """
        Récupère un itineraire permettant d'aller de origin à destination à une date donnée.
    """
    date_str = jour + "T" + heure
    return call_recherche_itineraire(origin=origin, destination=destination, date=date_str)
