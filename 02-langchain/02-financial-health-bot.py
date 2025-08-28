from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def create_financial_chain():
    prompt = ChatPromptTemplate([
        ("system", """You are an experienced financial advisor in India who specializes in
         personal finanace management. Analyze the customer's financial situation and provide
         detailed insights. Present the output in a clean format with clear sections."""),
        
        ("human", """Perform initial financial analysis for the client in India:
        - Monthly Income: {monthly_income}
        - Monthly Expenses: {monthly_expenses}
        - Current Savings: {current_savings}
        
        Following is the expected output
        A detailed financial analysis in markdown format including:
        - Current Financial Health Assessment
        - Cash Flow Analysis
        - Savings Potential
        - Risk Capacity Evaluation""")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    return prompt | llm | StrOutputParser()


st.set_page_config(
    page_title = "Financial Health Analysis",
    page_icon = "💰",
    layout = "wide" 
)

st.title("Personal Financial Health Analysis")

with st.sidebar:
    st.header("Enter Your Financial Details")
    monthly_income = st.number_input("Monthly Income (₹)", min_value=0)
    monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=0)
    current_savings = st.number_input("Current Savings (₹)", min_value=0)
    submit_button = st.button("Submit")
    
if(submit_button):
    with st.spinner("Analyzing your Financial Health"):
        inputs = {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "current_savings": current_savings
        }
        
        chain = create_financial_chain()
        result = chain.invoke(inputs)
        
        st.markdown(result)
else:
    st.info("Enter your financial details and click submit button")


