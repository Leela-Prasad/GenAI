from langtrace_python_sdk import langtrace
import os
from flows import FinancialAdvisorFlow
from crewai.llm import LLM
from dotenv import load_dotenv

def main():
    load_dotenv()
    langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))
    
    # llm = LLM("gpt-4o-mini")
    
    initial_state = {
        "monthly_income": 75000,
        "monthly_expenses": 45000,
        "current_savings": 200000,
        "risk_tolerance": "moderate",
        "investment_years": 15
    }
    flow = FinancialAdvisorFlow()
    result = flow.kickoff(inputs=initial_state)
    
    print("Final Result", result)
    
if __name__ == "__main__":
    main()