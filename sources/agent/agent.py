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
llm_with_tools = llm.bind_tools([get_itineraire])

custom_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""
                Vous êtes un assistant qui permet à un usager d'ile de France de trouver son
                itineraire dans les transports d'ile de France.

                Nous sommes le {datetime.now().strftime("%Y-%m-%d")}.
                Si l'utilisateur n'en fournit pas, considère que c'est la date et heure de départ.

                Répond à l'utilisateur en 3 lignes maximum, en langage naturel, le texte sera lu.
            """,
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

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


def invoke_agent(message: str) -> str:

    result = agent_executor.invoke({"input": message, "chat_history": CHAT_HISTORY})

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
        )
    )
