from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

verification = Task(
    description="Verify the document at path '{file_path}'. Ensure it is a valid financial report and extract the core financial figures.",
    expected_output="A summary confirming the document type and a brief overview of the main financial metrics found.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool]
)

analyze_financial_document = Task(
    description="Analyze the verified financial document at '{file_path}' to address the user's query: '{query}'. Focus on the actual data provided.",
    expected_output="A detailed, accurate financial analysis addressing the user's query, backed by specific numbers from the document.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    context=[verification]
)

risk_assessment = Task(
    description="Review the financial data at '{file_path}' in the context of the user's query: '{query}'. Identify any realistic market, operational, or financial risks.",
    expected_output="A professional risk assessment report detailing potential vulnerabilities and mitigation strategies.",
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool],
    context=[analyze_financial_document]
)

investment_analysis = Task(
    description="Based on the analysis and risk assessment, provide actionable investment recommendations regarding the user's query: '{query}'.",
    expected_output="A comprehensive investment recommendation plan, including risk-adjusted expected outcomes and verifiable data points.",
    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool],
    context=[analyze_financial_document, risk_assessment]
)