from crew import FinAdvisor
from dotenv import load_dotenv

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
    load_dotenv()
    run()