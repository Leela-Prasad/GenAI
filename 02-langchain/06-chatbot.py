from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
from uuid import uuid4
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, ConfigurableFieldSpec
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

if "store" not in st.session_state:
    # Needs to load user store from db
    st.session_state.store = {}

# This Needs to be passed as parameter   
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid4())
    
# This Needs to be passed as parameter
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid4())

if "counter" not in st.session_state:
    st.session_state.counter = 1    
    
if "conversations" not in st.session_state:
    st.session_state.conversations = [(str(st.session_state.conversation_id), "Conversation " + str(st.session_state.counter))]
    st.session_state.counter += 1

def get_session_history(user_id: str, converstaion_id: str) -> ChatMessageHistory:
    if (user_id, converstaion_id) not in st.session_state.store:
        st.session_state.store[(user_id, converstaion_id)] = ChatMessageHistory()
    return st.session_state.store[(user_id, converstaion_id)]


def get_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are helpful assistant, Answer all questions to best of your ability in {language}"),
        MessagesPlaceholder(variable_name="my_chat_history"),
        ("user", "{myinput}")
    ]) 
    
    model = ChatOpenAI(model="gpt-4o-mini")
    
    return RunnableWithMessageHistory(prompt | model, get_session_history, 
                                        input_messages_key="myinput",
                                        history_messages_key="my_chat_history",
                                        history_factory_config=[
                                            ConfigurableFieldSpec(id="user_id", annotation=str),
                                            ConfigurableFieldSpec(id="converstaion_id", annotation=str)
                                        ])
    
    

def create_new_conversation():
    new_conv_id = str(uuid4())
    st.session_state.conversations.append((new_conv_id, "Conversation " + str(st.session_state.counter)))
    st.session_state.counter += 1
    st.session_state.conversation_id = new_conv_id
    

st.title("Chatbot")
with st.sidebar:
    st.subheader("Conversations")
    if st.button("New Conversation"):
        create_new_conversation()
    
    conv_ids, conv_titles = map(list, zip(*st.session_state.conversations))
    selected_conv_title = st.selectbox("Select Conversation", 
                            options=conv_titles,
                            index=conv_ids.index(st.session_state.conversation_id) 
                        )
    
    selected_conv_id = conv_ids[conv_titles.index(selected_conv_title)]
    if selected_conv_id != st.session_state.conversation_id:
        st.session_state.conversation_id = selected_conv_id
    
    
chain = get_chain()
content = st.chat_input("What's in your mind...")
if content:
    config = {"configurable": {"user_id": st.session_state.user_id, "converstaion_id": st.session_state.conversation_id}}
    result = chain.invoke({
                "language": "english",
                "myinput": content
            },
            config=config)

messages = chain.get_session_history(st.session_state.user_id, st.session_state.conversation_id).messages
for message in messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)    
