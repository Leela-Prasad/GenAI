from crewai.tools import BaseTool
from textwrap import dedent
import sqlite3
import json

class CustomerInfoTool(BaseTool):
    name: str = "Customer Information Tool"
    description: str = dedent("""
                              Fetches customer financial information from the database.
                              Use this tool when you need to get detailed financial information about a customer.
                              Input should be a customer ID number.
                              """)
    
    # Need to override this run method for custom tool
    # def _run(self, customer_id: int) -> dict:
    #     return {
    #     "customerId": 1,    
    #     "salary": "150000",
    #     "expenses": "80000",
    #     "savings": "500000",
    #     "investments": "1000000",
    #     "loans": "2000000",
    #     "dependents": "2"
    # }
    
    def _run(self, customer_id: int) -> str:
        try:
            conn = sqlite3.connect('financial_advisor.db')
            cursor = conn.cursor()
            
            query = """
            SELECT 
                c.customer_id, c.name, c.age, c.occupation, 
                c.risk_profile, c.annual_income,
                f.monthly_salary, f.monthly_expenses, 
                f.current_savings, f.current_investments, 
                f.outstanding_loans, f.number_of_dependents
            FROM customers c
            JOIN financial_details f ON c.customer_id = f.customer_id
            WHERE c.customer_id = ?
            """
            
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()
            
            if not result:
                return json.dumps({"error": "Customer not found"})
                
            customer_info = {
                "customer_id": result[0],
                "name": result[1],
                "age": result[2],
                "occupation": result[3],
                "risk_profile": result[4],
                "annual_income": result[5],
                "monthly_salary": result[6],
                "monthly_expenses": result[7],
                "current_savings": result[8],
                "current_investments": result[9],
                "outstanding_loans": result[10],
                "number_of_dependents": result[11]
            }
            
            return json.dumps(customer_info, indent=2)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            conn.close()