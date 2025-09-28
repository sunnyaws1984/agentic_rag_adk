# rag_agent/agent.py
import os
from google.adk.agents import Agent
from rag_agent.rag_utils import get_retriever
from .prompt import return_instructions_root
from dotenv import load_dotenv

load_dotenv()
os.chdir(os.path.dirname(__file__))
pdf_path = os.path.abspath("data/sample.pdf")
retriever = get_retriever(pdf_path)

def search_pdf(query: str):
    """Search and retrieve relevant context from the PDF"""
    docs = retriever.get_relevant_documents(query)  # get the top matching document chunks back
    return "\n\n".join([doc.page_content for doc in docs]) # The final combined string is returned

root_agent = Agent(
    name="pdf_rag_agent",
    model="gemini-2.0-flash",
    description=(
        "You are a helpful assistant. "
        "Always answer user questions using the retrieved PDF context."
    ),
    instruction=return_instructions_root(),
    tools=[search_pdf],
)
