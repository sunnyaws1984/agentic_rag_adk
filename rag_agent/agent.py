# rag_agent/agent.py
import os
from google.adk.agents import Agent
from rag_agent.rag_utils import get_retriever
from .prompt import return_instructions_root
from dotenv import load_dotenv

load_dotenv()
os.chdir(os.path.dirname(__file__))  # Change working directory to the current file's directory
pdf_path = os.path.abspath("data/sample.pdf")
retriever = get_retriever(pdf_path)

def search_pdf(query: str) -> str:
    """
    Search and retrieve relevant context from the PDF.
    Compatible with LangChain v0.2+ retrievers.
    """
    docs = retriever.invoke(query)  # Runnable-style retrieval

    if not docs:
        return ""

    return "\n\n".join(doc.page_content for doc in docs)


root_agent = Agent(
    name="pdf_rag_agent",
    model="gemini-2.5-flash",
    description=(
        "You are a helpful assistant. "
        "Always answer user questions using the retrieved PDF context."
    ),
    instruction=return_instructions_root(),
    tools=[search_pdf],
)
