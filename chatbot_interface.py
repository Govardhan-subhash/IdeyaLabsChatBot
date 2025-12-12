import os
import sys
from dotenv import load_dotenv

from chroma_setup import get_chroma_vector_store, add_documents_to_chroma
from langchain_pipeline import create_rag_pipeline
from web_scraper import scrape_and_chunk

# Load env variables
load_dotenv()

def main():
    print("Initializing IdeyaLabs Chatbot...")
    
    # 1. Setup Vector Store
    try:
        vector_store = get_chroma_vector_store()
    except Exception as e:
        print(f"Failed to initialize vector store: {e}")
        return

    # 2. Check if we need to ingest data
    # Simple check: if collection is empty or force reload requested
    # For this demo, we'll check if it has documents. 
    # Note: Chroma's count() might be useful but let's just ask user or check blindly.
    # We will assume if "ideyalabs.com" is not in metadata, we might want to scrape.
    
    # Checking count (naive approach for this script)
    collection_count = vector_store._collection.count()
    print(f"Current collection count: {collection_count}")
    
    if collection_count == 0:
        print("Vector store is empty. Starting web scraping...")
        start_url = "https://ideyalabs.com/"
        print(f"Scraping {start_url}...")
        
        try:
            chunked_docs = scrape_and_chunk(start_url, max_depth=1)
            if chunked_docs:
                print(f"Scraped {len(chunked_docs)} chunks. Ingesting...")
                add_documents_to_chroma(vector_store, chunked_docs)
            else:
                print("No data scraped.")
        except Exception as e:
            print(f"Error during scraping/ingestion: {e}")

    # 3. Setup RAG Pipeline
    qa_chain = create_rag_pipeline(vector_store)
    
    print("\nChatbot is ready! Type 'exit' to quit or 'scrape' to force re-scrape.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if user_input.lower() == "scrape":
                print("Force scraping...")
                chunked_docs = scrape_and_chunk("https://ideyalabs.com/", max_depth=1)
                add_documents_to_chroma(vector_store, chunked_docs)
                print("Done.")
                continue

            response = qa_chain.invoke({"query": user_input})
            print(f"Chatbot: {response['result']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()