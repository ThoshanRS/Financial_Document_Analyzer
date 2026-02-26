from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

from pathlib import Path



from crewai import Agent


# force correct .env path
# env_path = Path(__file__).resolve().parent / ".env"
# load_dotenv(dotenv_path=env_path)

# from langchain_google_genai import ChatGoogleGenerativeAI

from tools import FinancialDocumentTool, InvestmentTool, RiskTool, search_tool




# OPENAI Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# GEMINI LLM initialization
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     temperature=0.1,
# )


# GROQ LLM initialization
# llm = ChatOpenAI(
#     model="groq/llama-3.1-8b-instant",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url="https://api.groq.com/openai/v1",
#     temperature=0.1,
# )

# Shared tools
tools = [
    FinancialDocumentTool.read_data_tool,
    InvestmentTool.analyze_investment_tool,
    RiskTool.create_risk_assessment_tool,
    search_tool,
]

# ---------------------------------------------------
# Financial Analyst
# ---------------------------------------------------
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents accurately and provide highly accurate, data-driven investment advice and market analysis based on the user query.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned Senior Financial Analyst with decades of experience at top-tier investment banks. "
        "You excel at analyzing complex financial documents, extracting key metrics, and providing actionable, "
        "regulatory-compliant investment insights. You rely strictly on verifiable facts."
    ),
    tools=tools,
    llm=llm,
    allow_delegation=True
)

# ---------------------------------------------------
# Document Verifier
# ---------------------------------------------------
verifier = Agent(
    role="Financial Document Verifier",
    goal="Thoroughly verify whether the uploaded document is a valid financial report and ensure extracted insights are accurate.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous compliance officer and financial document verifier. "
        "You ensure that all data analyzed is accurate and properly classified before it is used for investment decisions."
    ),
    tools=tools,
    llm=llm,
    allow_delegation=True
)

# ---------------------------------------------------
# Investment Advisor
# ---------------------------------------------------
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide sound, risk-adjusted investment recommendations based on financial analysis.",
    verbose=True,
    backstory=(
        "You are a Certified Financial Planner known for prudent, evidence-based investment strategies."
        "You always prioritize client risk tolerance and regulatory compliance."
    ),
    tools=tools,
    llm=llm,
    allow_delegation=False
)

# ---------------------------------------------------
# Risk Assessor
# ---------------------------------------------------
risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify and quantify financial and operational risks from corporate documents.",
    verbose=True,
    backstory=(
        "You are a Chief Risk Officer specializing in enterprise risk management and volatility analysis."
         "You accurately assess volatility, market conditions, and operational risks."
    ),
    tools=tools,
    llm=llm,
    allow_delegation=False
)