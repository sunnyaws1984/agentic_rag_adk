## 🚀 Setup Instructions

### 1. Clone the project
```bash
git clone https://github.com/sunnyaws1984/agentic_rag_adk.git
cd agentic_rag_adk 

2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
source .venv/Scripts/activate   # GIT BASH

3. Install Google ADK :

Install Python 3.13 as pre-requisite
pip install uv
uv pip install langchain langchain-community faiss-cpu sentence-transformers pypdf google-adk
or
pip install -r requirements.txt
uv pip install -r requirements.txt (Speed up the installations)

4. Run below commands:

adk web
open http://127.0.0.1:8000 in browser 

🧩 Sample Queries to test this RAG Application:

Can you share work from home policy of SPIL ?
Can you please summarize Probation and Confirmation policy ?