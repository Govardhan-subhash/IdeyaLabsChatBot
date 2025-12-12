from chroma_setup import get_chroma_vector_store, add_documents_to_chroma
from langchain_pipeline import create_rag_pipeline
from web_scraper import scrape_and_chunk
import sys

def verify_system():
    print("Starting verification (non-interactive)...")
    
    # 1. Initialize DB
    vector_store = get_chroma_vector_store()
    print("Vector Store initialized.")
    
    # 2. Add dummy data for test if empty
    if vector_store._collection.count() == 0:
        print("Adding test data...")
        test_docs = [{
            "page_content": "IdeyaLabs is a technology company specializing in AI and software development.",
            "metadata": {"source": "test_data"}
        }]
        add_documents_to_chroma(vector_store, test_docs)
    
    # 3. Test Query
    print("Testing Query...")
    qa_chain = create_rag_pipeline(vector_store)
    response = qa_chain.invoke({"query": "What does IdeyaLabs specialize in?"})
    
    print(f"Query Response: {response['result']}")
    
    if "AI" in response['result'] or "software" in response['result']:
        print("VERIFICATION PASSED")
    else:
        print("VERIFICATION FAILED (Response didn't contain expected keywords)")

if __name__ == "__main__":
    verify_system()
