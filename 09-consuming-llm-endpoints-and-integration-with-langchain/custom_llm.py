from langchain.chat_models.base import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from typing import List
import requests

class CustomLLM(BaseChatModel):
    endpoint: str
    model: str
    
    @property
    def _llm_type(self) -> str:
        return "Custom LLM"
    
    def _generate(self, messages, stop=None, **kwargs):
        payload_messages = []
        
        for msg in messages:
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            else:
                continue
            
            payload_messages.append({
                "role": role,
                "content": msg.content
            })

        response = requests.post(
            url=f"{self.endpoint}/v1/chat/completions",
            headers = {
                # "Authorization": ""
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": payload_messages,
                **kwargs
            }
        )
        
        response.raise_for_status()
        data = response.json()
        
        return ChatResult(generations=[ChatGeneration(
            message=AIMessage(content=data["choices"][0]["message"]["content"])
        )])
        
        
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    HumanMessage(content="My Name is Leela"),
    AIMessage(content="Nice to meet you, Leela! How can I assist you today?"),
    HumanMessage(content="What is my Name")
])


llm = CustomLLM(
    endpoint = "http://127.0.0.1:8000",
    model="gpt-4o-mini"
)

response = llm.invoke(prompt.format_messages())
print(response)