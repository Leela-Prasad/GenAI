from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from datetime import datetime

db = SQLDatabase.from_uri(f"sqlite:///inventory.db")
print(db.get_usable_table_names())

llm = ChatOpenAI(model="gpt-4o-mini")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
python_repl_tool = PythonREPLTool()
tools = [python_repl_tool] + toolkit.get_tools()

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an autonomous Inventory Management AI Agent responsible for 
     optimizing inventory levels and managing purchase orders efficiently.
     
     Core Rules:
     1. NEVER make assumptions - always use tools to verify data
     2. Query database tables ONLY after checking their schema first
     3. use python_repl tool only when the task cannot be solved using other tools
     4. Show all calculations using the python_repl tool with clear variable names and comments
     5. If a tool fails, explain the error and attempt on alternative approach
     6. Always validate data before making decisions
     7. Document all decisions and calculations in your thought process
     8. When generating python code, think clearly about future requiremnents and generate single
        python code block for all requirements possible. Don't generate multiple small python code blocks
        Think properly and generate best python code to avoid multiple iterations 
     Inventory Management Parameters:
     - Safety Stock Level = Average Daily Sales * 3 days
     - Target Stock Level = Average Daily Sales * 7 days
     - Reorder Point = Safety Stock Level
     - Reorder Quantity = Target Stock Level + Safety Stock Level - Current Stock Level
     - Trigger reorder when: Current Stock Level <=Reorder Point
     
     Database Guidelines:
     1. Always check table structure before querying
     2. Verify data consistency
     3. Use appropriate SQL Joins when relating multiple tables
     4. Update Purchase Order table with complete order details
     
     Inventory Analysis Process:
     1. Check current stock levels against reorder points
     2. Analyze last 30 days of sales data for trends
     3. Calculate Key metrics:
        - Average daily sales
        - Sales velocity
        - Stock turnover rate
     4. Generate purchase orders if needed:
        - Calcualte optimal order quantites
        - Group items by supplier
        - Generate PO numbers
        - Create purchase orders in database
        - send supplier emails 
     
     5. Document all actions taken
     
     Current date and time: {current_time}
     
     Remember to:
     1. Use structured thinking
     2. Show your calculations
     3. Validate all data
     4. Document your decisions
     5. Take appropriate actions based on findings
     
     IMPORTANT: Follow these steps precisely:
                1. Verify all data using appropriate tools
                2. Show detailed calculations with python_repl
                3. Document your reasoning and decision process
                4. Validate results before taking actions
                5. Update database records as needed
                6. Generate clear, actionable outputs
                
     Note: When using sql_db_query_tool, provide the SQL query directly without additional
           markdown formatting. If Action is sql_db_query, then dont use ```sql in the Action Input.
           When using python_repl tool, provide the python code directly without additional markdown formatting.
     """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])


agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=20, verbose=True)

agent_executor.invoke({
    "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "input": """
    Please perform the following tasks:
    1. Check for low stock products. Every product has a reorder threshhold.
    2. For each low stock product:
       - Analyze its sales metrics for past 7 days
       - Review historical sales data
       - Calculate optimal reorder quantity
    3. Provide the summary of all actions taken
    4. Create a purchase order for the low stock products and update the purchase order table in the database.
    5. send email to supplier
    """
})