from crewai.flow.flow import Flow, start, listen, router
from crew1 import InvestmentAnalysisCrew
from crew2 import WealthManagementCrew
from pydantic import BaseModel
from typing import Optional

class FinancialState(BaseModel):
    #Inputs
    monthly_income: float = 0.0
    monthly_expenses: float = 0.0
    current_savings: float = 0.0
    risk_tolerance: str = "moderate"
    investment_years: int = 15
    
    #Results from Crew
    investment_analysis_result: Optional[str] = None
    wealth_management_result: Optional[str] = None
    
    #Flow Control
    analysis_completed: bool = False
    error_occurred: bool = False
    error_message: str = ""
    
    
class FinancialAdvisorFlow(Flow[FinancialState]):
    
    def __init__(self):
        super().__init__()
        self.investment_crew = InvestmentAnalysisCrew().crew()
        self.wealth_crew = WealthManagementCrew().crew()
        
    # @classmethod
    # def parse_input(cls, data: Dict[str, Any]) -> FinancialState:
    #     """Parse input dictionary into FinancialState"""
    #     return FinancialState(**data)
    
    @start()
    def invoke_investment_crew(self):
        print("Starting Financial Advisory Process")
        print(f"Analyzing financial situation for client with:")
        print(f"Monthly Income: INR {self.state.monthly_income}")
        print(f"Monthly Expenses: INR{self.state.monthly_expenses}")
        print(f"Current Savings: INR {self.state.current_savings}")
        
        try:
            inputs = {
                "monthly_income": self.state.monthly_income,
                "monthly_expenses": self.state.monthly_expenses,
                "current_savings": self.state.current_savings,
                "risk_tolerance": self.state.risk_tolerance,
                "investment_years": self.state.investment_years
            }
            
            crew1_result = self.investment_crew.kickoff(inputs=inputs)
            self.state.investment_analysis_result = crew1_result.raw
            self.state.analysis_completed = True
        except Exception as e:
            self.state.error_occurred = True
            self.state.error_message = str(e)
            
    @router(invoke_investment_crew)
    def route_flow(self):
        if self.state.error_occurred:
            return "handle_error"
        elif self.state.analysis_completed:
            return "process_wealth_management"
        else:
            return "handle_incomplete_analysis"


    @listen("process_wealth_management")
    def invoke_wealth_crew(self):
        print("Processing Wealth Management Plan")
        
        try:
            inputs = {
                "crew_one_output": self.state.investment_analysis_result
            }
            
            crew2_result = self.wealth_crew.kickoff(inputs=inputs)
            self.state.wealth_management_result = crew2_result.raw
            
            print("\nInvestment Analysis Results:")
            print(self.state.investment_analysis_result)
            print("\nFinal Wealth Management Plan:")
            print(self.state.wealth_management_result)
            return self.state
        except Exception as e:
            self.state.error_occurred = True
            self.state.error_message = str(e)
            return "handle_error"
        
    @listen("handle_error")
    def handle_error(self):
        print(f"Error occurred during financial advisory process:")
        print(f"Error message: {self.state.error_message}")
        print("Please review the error and try again")
        
    @listen("handle_incomplete_analysis")
    def handle_incomplete_analysis(self):
        print("Error: Investment analysis was not completed successfully")
        print("Please ensure all required data is provided and try again")