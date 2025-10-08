from langserve import RemoteRunnable

llm = RemoteRunnable("http://localhost:8000/invoke-llm")

response = llm.invoke("tell me about in India in 1 sentence")
print(response)

response2 = llm.batch(["tell me about trump in one sentence", "tell me about in India in 1 sentence"])
print(response2)