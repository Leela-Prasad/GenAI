import gradio as gr
import tempfile

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

embeddings = HuggingFaceEmbeddings()

def load_pdf_into_vectorstore(file: tempfile):
    file_path = file.name
    
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10, separator="")
    chunks = text_splitter.split_documents(documents=documents)
    
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="mychroma_db_123")
    return "Document uploaded successfully. You can chat now"


def get_response(query, history: list) -> tuple:
    vector_store = Chroma(persist_directory="mychroma_db_123", embedding_function=embeddings)
    message = """
            Answer this question using the provided context only.
            If the information is not available in the context, justy reply with "I dont know"
            {input}
            Context: {context}
          """
    
    prompt = ChatPromptTemplate.from_messages([
                ("human", message)
            ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(vector_store.as_retriever(), qa_chain)
    
    response = rag_chain.invoke({"input": query})
    history.append((query, response["answer"]))
    
    return "",history
    
    

with gr.Blocks() as app:
    with gr.Row():
        with gr.Column():
            file = gr.components.File(label="Upload your pdf file",
                                      file_count="single",
                                      file_types=[".pdf"])
            upload = gr.components.Button("Upload", variant="primary")
        
        #Next Column    
        upload_status_label = gr.components.Textbox()
    
    #Next Row    
    chatbot = gr.Chatbot(label="Talk to the document")
    msg = gr.Textbox()
    
    #upload.click(function_to_invoke, [input1, input2, ...], [output1, output2, ...])
    upload.click(load_pdf_into_vectorstore, [file], [upload_status_label])
    
    #msg.submit(function_to_invoke, [input1, input2, ...], [output1, output2, ...])
    msg.submit(get_response, [msg, chatbot], [msg, chatbot])
    
app.launch(debug=True)
    