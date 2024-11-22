from datetime import datetime
import os

from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI

from sources.agent.tools.get_itineraire import get_itineraire


from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
AZURE_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
API_KEY = os.getenv('AZURE_OPENAI_API_KEY')

MEMORY_KEY = "chat_history"
CHAT_HISTORY = []

TOOLS = [get_itineraire]

azure_open_ai_parameters = {
    "api_version": API_VERSION,
    "azure_endpoint": AZURE_ENDPOINT,
    "api_key": API_KEY
}

llm = AzureChatOpenAI(
    **azure_open_ai_parameters,
    model=os.getenv('AZURE_OPENAI_MODELS'),
    temperature=0.2,
)
llm_with_tools = llm.bind_tools(TOOLS)

custom_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""
                Vous êtes un assistant qui permet à un usager d'ile de France de trouver son
                itineraire dans les transports d'ile de France.

                Nous sommes le {datetime.now().strftime("%Y-%m-%d")}.
                Il est {datetime.now().strftime("%H:%M:%S")}.
                Si l'utilisateur n'en fournit pas, considère que c'est la date et heure de départ.

                Si l'utilisateur ne précise pas de point de départ, utilise sa geolocation si elle t'est donnée,
                si elle est inconnue demande lui de l'activer dans l'interface, n'invente rien.

                Répond à l'utilisateur en 3 lignes maximum, en langage naturel, le texte sera lu.
            """,
        ),
        ("system", "User location: {user_location}"),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        "user_location": lambda x: x["user_location"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | custom_prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True)


def invoke_agent(message: str, location: str) -> str:

    result = agent_executor.invoke({"input": message, "user_location": location, "chat_history": CHAT_HISTORY})

    CHAT_HISTORY.extend(
        [
            HumanMessage(content=message),
            AIMessage(content=result["output"]),
        ]
    )

    return result["output"]


if __name__ == "__main__":
    invoke_agent(
        message=(
            "Comment aller du 34 avenue de l'Opéra Paris"
            "au 89 rue saint Antoine Paris demain à 14h ?"
        ),
        location=None
    )
