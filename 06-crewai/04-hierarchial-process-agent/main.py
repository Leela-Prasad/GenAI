from langtrace_python_sdk import langtrace
from dotenv import load_dotenv
import os

load_dotenv()
langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))

from crew import WealthManagementCrew

def run():
    
    inputs = {
        "monthly_income": "75000",
        "monthly_expenses": "45000",
        "current_savings": "200000",
        "risk_tolerance": "moderate",
        "investment_years": "15"
    }
    
    WealthManagementCrew().crew().kickoff(inputs=inputs)
    

if __name__ == "__main__":
    run()