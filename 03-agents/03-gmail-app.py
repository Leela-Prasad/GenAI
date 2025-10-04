#pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_community.tools.gmail import GmailCreateDraft, GmailGetMessage, GmailSearch
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta

load_dotenv()


def gmail_oauth_flow():
    scopes = ["https://www.googleapis.com/auth/gmail.modify"]
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
    creds = flow.run_local_server(port=0)
    
    return build("gmail", "v1", credentials=creds)
    
    
service = gmail_oauth_flow()

tools = [
    GmailCreateDraft(api_resource=service),
    GmailGetMessage(api_resource=service),
    GmailSearch(api_resource=service)
]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant that helps manage emails.
     Your task includes.
     1. Reading emails
     2. Creating appropriate draft responses
     3. Summarizing email content
     
     Always be professional and courteous in drafts.
     When creating drafts, make sure to include:
     - A professional greeting
     - Clear and detailed content
     - A proper Signature
     """),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")
#gmail_search_query = f"is:unread after:{yesterday}"
gmail_search_query = f"is:unread from:leelaprasad.jagu@gmail.com after:{yesterday}"

agent_executor.invoke({"input": f"""
                       1. Search for 5 most recent emails matching: {gmail_search_query}
                       2. For each email:
                          - Read the content
                          - summary of actions taken
                          - Create and appropriate draft message
                       """})