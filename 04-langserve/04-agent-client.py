from langserve import RemoteRunnable

agent = RemoteRunnable("http://localhost:8000/my-agent")
response = agent.invoke({
    "input": "what is 2+3 multiplied by 4"
})

print(response)