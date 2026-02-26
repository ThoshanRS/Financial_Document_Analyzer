# tools.py

import os
import requests
from dotenv import load_dotenv
from crewai.tools import tool
from pypdf import PdfReader
# from crewai_tools import SerperDevTool
# from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool

# Load environment variables
load_dotenv()

# ---------------------------------------------------
# Search Tool (Web Search Capability)
# ---------------------------------------------------
# search_tool = SerperDevTool()


# ===================================================
# Financial Document Reader Tool
# ===================================================

class FinancialDocumentTool:
    @tool("Read Financial Document")
    def read_data_tool(path: str = "data/sample.pdf") -> str:
        """
        Reads and extracts text from a financial PDF document.

        Args:
            path (str): Path to the PDF file.

        Returns:
            str: Cleaned financial document text.
        """

        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")

            reader = PdfReader(path)
            pages_text = []

            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text()

                if text:
                    # Normalize formatting
                    content = text.replace("\t", " ").strip()
                    content = re.sub(r"\n+", "\n", content)

                    pages_text.append(f"[Page {i}]\n{content}")

            if not pages_text:
                raise ValueError("No readable text found in PDF.")

            document_text = "\n\n".join(pages_text)

            return f"""
FINANCIAL DOCUMENT CONTENT
==========================
{document_text}
"""

        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {str(e)}")


# ===================================================
# Investment Analysis Tool
# ===================================================

from crewai.tools import tool
import re

class InvestmentTool:

    @tool("Analyze Investment Insights")
    def analyze_investment_tool(financial_document_data: str) -> str:
        """
        Performs basic investment insight extraction.
        """

        # Efficient cleanup (replaces inefficient loop)
        text = re.sub(r"\s+", " ", financial_document_data).lower()

        insights = []

        if "revenue" in text:
            insights.append("Revenue information identified.")

        if "net income" in text or "profit" in text:
            insights.append("Profitability indicators detected.")

        if "cash flow" in text:
            insights.append("Cash flow metrics present.")

        if not insights:
            insights.append("Limited investment signals detected.")

        return "Investment Insights:\n" + "\n".join(insights)


# ===================================================
# Risk Assessment Tool
# ===================================================

class RiskTool:

    @tool("Assess Financial Risks")
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """
        Performs basic risk identification from document text.
        """

        text = financial_document_data.lower()
        risks = []

        if "decline" in text or "decrease" in text:
            risks.append("Potential performance decline mentioned.")

        if "uncertain" in text or "volatility" in text:
            risks.append("Market uncertainty detected.")

        if "increase in expenses" in text:
            risks.append("Rising cost risk identified.")

        if not risks:
            risks.append("No major risks explicitly found.")

        return "Risk Assessment:\n" + "\n".join(risks)
    

# Serper Search Tool (Custom)
# -----------------------------
@tool("Web Search")
def search_tool(query: str) -> str:
    """Search the web using Serper API."""

    api_key = os.getenv("SERPER_API_KEY")

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        json={"q": query},
    )

    data = response.json()

    results = []
    for item in data.get("organic", [])[:5]:
        results.append(f"{item['title']} - {item['link']}")

    return "\n".join(results)