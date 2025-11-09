from crewai.tools import BaseTool
from textwrap import dedent

class CustomerInfoTool(BaseTool):
    name: str = "Customer Information Tool"
    description: str = dedent("""
                              Fetches customer financial information from the database.
                              Use this tool when you need to get detailed financial information about a customer.
                              Input should be a customer ID number.
                              """)
    
    # Need to override this run method for custom tool
    def _run(self, customer_id: int) -> dict:
        return {
        "customerId": 1,    
        "salary": "150000",
        "expenses": "80000",
        "savings": "500000",
        "investments": "1000000",
        "loans": "2000000",
        "dependents": "2"
    }