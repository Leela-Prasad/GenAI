from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

## Loading
loader = PyPDFLoader("letter.pdf")
documents = loader.load()

## Chunking
text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=3, separator="\n")
chunks = text_splitter.split_documents(documents=documents)

## OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

## HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings()

## Chroma Vectorstore New DB 
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="chroma_db_with_huggingface")

## Chroma Vectorstore Loading Existing DB
vectorstore = Chroma(persist_directory="chroma_db_with_huggingface", embedding_function=embeddings)

## FAISS Vectorstore New DB
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("faiss_store")

## FAISS Vectorstore Loading Existing DB
vectorstore = FAISS.load_local("faiss_store", embeddings=embeddings, allow_dangerous_deserialization=True)


## Retrieval of chunks using Similarity Search
retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs = {"k": 4}
            )

result = retriever.invoke("what is the relieving date")
print("result", result)


message = """
            Answer this question using the provided context only.
            If the information is not available in the context, justy reply with "I dont know"
            {input}
            Context: {context}
          """

prompt = ChatPromptTemplate.from_messages([
    ("human", message)
])

llm = ChatOpenAI(model = "gpt-4o-mini")

## Augmenting Context without Document Stuffing
chain = {"input": RunnablePassthrough(), "context": retriever} | prompt | llm
response = chain.invoke("what is the relieving date")
print("response", response)

## Augmenting Context with Document Stuffing
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input": "what is the relieving date"})
print("response", response)
