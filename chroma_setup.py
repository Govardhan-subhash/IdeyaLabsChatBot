import os
from langchain_chroma import Chroma
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_chroma_vector_store(collection_name="gemini_rag_collection"):
    """
    Initializes and returns the Chroma vector store with HuggingFace embeddings.
    """
    # Using HuggingFace Embeddings (local) to avoid API quotas
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    return vector_store

def add_documents_to_chroma(vector_store, documents):
    """
    Adds documents to the Chroma vector store.
    
    Args:
        vector_store: The Chroma vector store instance.
        documents (list): List of dictionaries with 'page_content' and 'metadata'.
    """
    from langchain.docstore.document import Document
    
    docs = [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in documents]
    vector_store.add_documents(docs)
    print(f"Added {len(docs)} documents to the vector store.")

if __name__ == "__main__":
    # Example usage
    try:
        vector_store = get_chroma_vector_store()
        print("Chroma vector store initialized successfully.")
    except Exception as e:
        print(f"Error initializing Chroma: {e}")