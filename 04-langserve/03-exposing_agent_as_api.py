from dotenv import load_dotenv
from langchain.agents import tool
from langchain_tavily import TavilySearch
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langserve import add_routes
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Adds a and b"""
    return int(a) + int(b)


@tool
def subtract(a: int, b: int) ->int:
    """Subtracts b from a"""
    return int(a) - int(b)

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b"""
    return int(a) * int(b)

tavily_search_tool = TavilySearch(max_results=3)

tools = [tavily_search_tool, add, subtract, multiply]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI.
                You should not use tools parallely
                You should not make your own conclusions even if it is easy, instead use appropriate tools"""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

class Input(BaseModel):
    input: str

class Output(BaseModel):
    output: Any

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

app = FastAPI()
add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output),
    path="/my-agent"
)