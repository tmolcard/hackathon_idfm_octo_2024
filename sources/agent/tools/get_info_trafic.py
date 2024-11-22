from typing import Annotated

from sources.api.api_prim import call_info_trafic

from langchain_core.tools import tool


@tool
def get_info_trafic(
    ligne: Annotated[
        str, "Ligne de transport sur laquelle nous cherchons des informations sans le type (métro/rer/...)"
             "Exemple RER E -> E"]
) -> str:
    """
        Récupère les informations sur les potentiels problèmes des moyens de transport.
    """
    return call_info_trafic(ligne)
