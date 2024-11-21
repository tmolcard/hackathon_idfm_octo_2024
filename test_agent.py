from datetime import datetime
import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from langchain.agents import load_tools
from langchain_core.tools import tool
from typing import Annotated, List

from test_api import call_riti


from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

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
    temperature=0.5,
)


@tool
def get_itineraire(
    origin: Annotated[
        str, "Point de départ sous la forme d'une adresse."],
    destination: Annotated[
        str, "Destination de l'itineraire recherché sous la forme d'une adresse."],
    jour: Annotated[
        str, "Jour à laquelle l'utilisateur veut partir au format : YYYYmmddTHHMMSS"]
) -> str:
    """
        Récupère un itineraire permettant d'aller de origin à destination à une date donnée.
    """
    return call_riti(origin=origin, destination=destination, jour=jour)


if __name__ == "__main__":

    MEMORY_KEY = "chat_history"

    custom_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
                    Nous sommes le {datetime.now().strftime("%Y-%m-%d")}
                    Vous êtes un assistant qui permet à un usager d'ile de france de trouver son itineraire
                    dans les transports d'ile de france.

                    Répond à partir du json renvoyé par la fonction à ta disposition.
                """,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind_tools([get_itineraire])

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | custom_prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=[get_itineraire], verbose=True)
    chat_history = []

    while True:
        input = "soit plus succinct"
        result = agent_executor.invoke({"input": input, "chat_history": chat_history})

        chat_history.extend(
            [
                HumanMessage(content=input),
                AIMessage(content=result["output"]),
            ]
        )
