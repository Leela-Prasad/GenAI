# pip install langserve uvicorn sse_starlette

from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini")

add_routes(app, llm, path="/invoke-llm")
