from langtrace_python_sdk import langtrace
from dotenv import load_dotenv
import os

load_dotenv()
langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))


from crew import FinAdvisor

def run():
    inputs = {
        "salary": "₹1,50,000",
        "expenses": "₹80,000",
        "savings": "₹5,00,000",
        "investments": "₹10,00,000",
        "loans": "₹20,00,000",
        "dependents": "2"
    }
    
    FinAdvisor().crew().kickoff(inputs=inputs)
    

if __name__ == "__main__":
    run()