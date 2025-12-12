from chroma_setup import get_chroma_vector_store
from langchain_pipeline import create_rag_pipeline
import sys

def main():
    print("--- Starting Chat Verification (No Scraping) ---")
    
    # 1. Initialize Vector Store (Use existing persistence)
    try:
        vector_store = get_chroma_vector_store()
        print(f"Vector Store initialized. Collection count: {vector_store._collection.count()}")
    except Exception as e:
        print(f"Failed to load vector store: {e}")
        return

    # 2. Setup RAG Pipeline
    qa_chain = create_rag_pipeline(vector_store)
    
    # 3. CLI Loop
    print("\nChatbot Ready. Type 'exit' to quit.")
    while True:
        try:
            query = input("\nYou: ")
            if query.lower() in ["exit", "quit"]:
                break
            
            result = qa_chain.invoke({"query": query})
            print(f"Bot: {result['result']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
