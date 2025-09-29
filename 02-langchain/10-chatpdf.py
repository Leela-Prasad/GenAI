import streamlit as st
import os
import tempfile
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None 

def load_pdf_into_vectorstore(uploaded_file):
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name
        
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10, separator="")
    chunks = text_splitter.split_documents(documents=documents)
    
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(documents=chunks, 
                                         embedding=embeddings, persist_directory="chroma239")
    
    os.unlink(file_path)
    st.session_state.vector_store = vector_store
    
    return True, "Documents uploaded and indexed successfully"
    

def get_response(query):
    if st.session_state.vector_store is None:
        return "Please upload a document first"
    
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory="chroma239",
                          embedding_function=embeddings)
    
    message = """
            Answer this question using the provided context only.
            If the information is not available in the context, justy reply with "I dont know"
            {input}
            Context: {context}
          """
          
    prompt = ChatPromptTemplate([
        ("human", message)
    ])    
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    qa_chain = create_stuff_documents_chain(llm, prompt)
    retriever_chain = create_retrieval_chain(vector_store.as_retriever(), qa_chain)
    
    response = retriever_chain.invoke({"input": query})
    return response["answer"]
    
        
st.title("Chat with PDF")
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Processing Document..."):
                status, message = load_pdf_into_vectorstore(uploaded_file)
                if status:
                    st.success(message)
                else:
                    st.error(message)
                    

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
prompt = st.chat_input("Ask a question about your document")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):    
        response = get_response(prompt)
        st.write(response)
        
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
            