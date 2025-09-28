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

Install Python 3.13.5 as pre-requisite
pip install google-adk
pip install langchain langchain-community faiss-cpu sentence-transformers pypdf
pip install google-generativeai

or

pip install -r requirements.txt

4. Run below commands:

adk web
open http://127.0.0.1:8000 in browser 
Query: Can you share work from home policy of SPIL ?