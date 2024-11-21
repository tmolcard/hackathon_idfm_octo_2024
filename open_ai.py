import openai
import json
import os
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain import LLMChain
from datetime import datetime
from langchain.prompts import PromptTemplate

API_KEY = os.environ["AZURE_OPENAI_API_KEY"]

ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

VERSION = os.environ["AZURE_OPENAI_API_VERSION"]

llm = AzureChatOpenAI(
    openai_api_version=VERSION,
    azure_endpoint=ENDPOINT,
    azure_deployment='gpt-4o-mini',
    temperature=0.5,
    max_tokens=200,
    timeout=60,
    max_retries=10,
    # model="gpt-35-turbo",
    # model_version="0125",
    # other params...
)

# Define the template
template = """
Vous êtes un assistant qui extrait des informations utiles d'une phrase en français.

Identifiez et retournez les informations suivantes :
- "heure" : L'heure mentionnée (au format "YYYYmmddTHHMMSS").
- "point_de_depart" : Le point de départ.
- "point_d_arrivee" : Le point d'arrivée.

L'heure doit être au format "YYYYmmddTHHMMSS".
Si une information est absente, remplacez-la par "null".

Le retour doit être sous cette forme : heure|point_de_depart|point_d_arrivee

Voici la phrase à analyser : "{question}"
"""

# Create the prompt template
prompt = PromptTemplate(template=template, input_variables=["question"])

# Define the chain
chain = LLMChain(prompt=prompt, llm=llm)

# Define the query
query = "Je veux me déplacer du 56 rue de bagnolet à chatelet demain 8h"

# Debugging: Print the rendered prompt
rendered_prompt = prompt.format(question=query)
print(f"Rendered Prompt:\n{rendered_prompt}")

# Get the response
response = chain.run(question=query)

# Print the agent's response
print(f"Agent Response: {response}")