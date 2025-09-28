import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_or_create_faiss(pdf_path: str, index_path: str = "faiss_index"):
    """Load FAISS index if it exists, otherwise create one from PDF with custom chunking."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    try:
        # Try to load an existing FAISS index from disk.
        # FAISS stores only vectors, so we must pass the same embedding model
        # to embed new queries in the same vector space as stored chunks.
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        # Note: Pickle deserialization can be unsafe if loading untrusted files.
    except Exception:
        # Otherwise: load the PDF, split it, embed chunks, and create a new FAISS index.
        loader = PyPDFLoader(pdf_path)       # Reads the PDF into LangChain Document objects (1 per page).
        docs = loader.load() # Load PDF into Document objects

        # Split long pages into smaller overlapping chunks for better embedding & retrieval.
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,   # max characters per chunk
            chunk_overlap=200  # overlap between chunks to preserve context
        )
        split_docs = splitter.split_documents(docs)

        # Create FAISS index:
        # - Convert each chunk into an embedding vector
        # - Store vectors in FAISS for fast similarity search
        # - Keep mapping back to original Document + metadata
        vectorstore = FAISS.from_documents(split_docs, embeddings)
        vectorstore.save_local(index_path)
        return vectorstore

# Note: `faiss_index/` is just a local folder where the FAISS vector database is stored.
# - If the folder exists: loads the index from disk.
# - If not: builds a new one from the PDF and saves it for future reuse.

def get_retriever(pdf_path: str, index_path: str = "faiss_index"):
    """
    Returns a retriever for use inside an ADK agent.
    """
    vectorstore = get_or_create_faiss(pdf_path, index_path)
    return vectorstore.as_retriever(search_kwargs={"k": 3})  # Finds the k=3 most similar chunks in FAISS.

    # PDF → Pages (Document) → Chunked Docs → Embeddings → FAISS Index (saved/loaded) → Retriever
