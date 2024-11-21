import os
from datetime import datetime

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from test_api import call_riti

API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
AZURE_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
API_KEY = os.getenv('AZURE_OPENAI_API_KEY')

azure_open_ai_parameters = {
    "api_version": API_VERSION,
    "azure_endpoint": AZURE_ENDPOINT,
    "api_key": API_KEY
}

llm = AzureChatOpenAI(
    **azure_open_ai_parameters,
    model=os.getenv('AZURE_OPENAI_MODELS'),
    temperature=0.9,
)

template_get_data = f"""
On est le {datetime.now().strftime("%Y%m%d")}
Vous êtes un assistant qui extrait des informations utiles d'une phrase en français. 
Voici une phrase : "{{input}}"

Identifiez et retournez les informations suivantes :
-date: La date mentionnée
-depart: Le point de départ
-arrivee: Le point d'arrivée

La date doit être au format "YYYYmmddTHHMMSS".
Si une information est absente, remplacez-la par "null".

Le retour doit être sous cette forme : heure|point_de_depart|point_d_arrivee
"""
custom_rag_prompt_get_data = PromptTemplate.from_template(template_get_data)


template_response = """
Voici un JSON contenant des données d'un trajet :
{response}

À l'aide de cette réponse, donne une réponse claire et concise contenant:
- Heure de départ.
- Heure d'arrivée.
- Durée totale du trajet.
- Liste des étapes du trajet, avec pour chaque étape :
  - Mode de transport (ex. : métro, RER, bus, marche).
  - Description ou instruction de l'étape.

Donnez la réponse sous forme d'un texte claire, comme si vous parliez directement à un utilisateur.
"""
custom_rag_prompt_response = PromptTemplate(input_variables=['response'], template=template_response)


def return_api(response):
    data = response.content.split('|')

    response_api = call_riti(origin=data[1], destination=data[2], jour=data[0])

    itineraire = response_api['journeys'][0][0]
    return {"response": {
            "duration": itineraire["duration"],
            "nombre changement": itineraire["nb_transfers"],
            "heure de départ": itineraire["departure_date_time"],
            "heure d'arrivée": itineraire["arrival_date_time"],
            "heure demandée": itineraire["requested_date_time"],
            "distance marche": itineraire["distances"]["walking"],
            "prix du trajet": itineraire["fare"],
            "itineraire": itineraire["sections"],
        }
    }


def get_response(response):
    return response.content


rag_chain = (
    {"input": RunnablePassthrough()}
    | custom_rag_prompt_get_data
    | llm
    | return_api
    | custom_rag_prompt_response
    | llm
    | get_response
)


def launch_rag(rag_chain, question):
    return rag_chain.invoke(question)


if __name__ == "__main__":
    launch_rag(rag_chain, "Je veux aller à La Défense depuis Chatelet à 17h")
