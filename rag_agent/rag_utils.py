import os
from typing import Optional

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_INDEX_PATH = "faiss_index"

# Embedding model (shared)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Returns a HuggingFace embedding model.
    Must be the same model used for both indexing and retrieval.
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# FAISS creation / loading

def get_or_create_faiss(pdf_path: str,index_path: str = DEFAULT_INDEX_PATH) -> FAISS:
    """
    Load a FAISS index from disk if it exists.
    Otherwise, create a new FAISS index from the given PDF and save it.
    """
    embeddings = get_embeddings()

    # If index already exists, load it
    if os.path.exists(index_path):
        return FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True,  # safe if index is trusted
        )

    # Otherwise, build index from PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    split_documents = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(split_documents, embeddings)
    vectorstore.save_local(index_path)

    return vectorstore

# Retriever creation

def get_retriever(pdf_path: str, index_path: str = DEFAULT_INDEX_PATH,):
    """
    Returns a LangChain retriever compatible with v0.2+ (Runnable interface).
    """
    vectorstore = get_or_create_faiss(pdf_path, index_path)

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )