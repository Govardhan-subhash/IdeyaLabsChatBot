# import os
# import json
# from web_scraper import scrape_website_recursively
# from chroma_setup import get_chroma_vector_store, add_documents_to_chroma
# from langchain_pipeline import create_rag_pipeline
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def main():
#     print("--- Starting Full Pipeline Verification ---")
    
#     # 1. Scrape Data
#     start_url = "https://ideyalabs.com/"
#     print(f"\n[Step 1] Scraping {start_url}...")
#     try:
#         # Increased depth to 3 to capture more subpages recursively
#         raw_data = scrape_website_recursively(start_url, max_depth=3)
#         print(f"Scraped {len(raw_data)} pages.")
#     except Exception as e:
#         print(f"Scraping failed: {e}")
#         return

#     # 2. Store Document (Save to file as requested)
#     print("\n[Step 2] Storing scraped data to 'scraped_data.json'...")
#     with open("scraped_data.json", "w", encoding="utf-8") as f:
#         json.dump(raw_data, f, ensure_ascii=False, indent=2)
#     print("Data saved to disk.")

#     # 3. Reading for Embeddings
#     print("\n[Step 3] Reading data for embedding generation...")
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunked_documents = []
    
#     for url, content in raw_data.items():
#         chunks = text_splitter.split_text(content)
#         for i, chunk in enumerate(chunks):
#             chunked_documents.append({
#                 "page_content": chunk,
#                 "metadata": {"source": url, "chunk_id": i}
#             })
#     print(f"Prepared {len(chunked_documents)} chunks.")

#     # 4. Inject into Vector DB
#     print("\n[Step 4] Injecting into Vector Database...")
#     try:
#         vector_store = get_chroma_vector_store()
#         # Check if already populated to avoid duplicates for this test run, or just add anyway
#         # For this test, we'll add.
#         add_documents_to_chroma(vector_store, chunked_documents)
#         print("Data injected into ChromaDB.")
#     except Exception as e:
#         print(f"Injection failed: {e}")
#         return

#     # 5. CLI Test
#     print("\n[Step 5] CLI Query Test")
#     qa_chain = create_rag_pipeline(vector_store)
    
#     print("Enter a query (or 'exit' to quit):")
#     while True:
#         query = input("Query> ")
#         if query.lower() in ["exit", "quit"]:
#             break
        
#         try:
#             result = qa_chain.invoke({"query": query})
#             print(f"Answer: {result['result']}\n")
#         except Exception as e:
#             print(f"Query error: {e}")

# if __name__ == "__main__":
#     main()


import json
from chroma_setup import get_chroma_vector_store
from langchain_pipeline import create_rag_pipeline

def main():
    print("--- Starting RAG Query Only Mode ---")

    # 1. Load existing Chroma DB
    print("\n[Step 1] Loading existing Chroma Vector Database...")
    try:
        vector_store = get_chroma_vector_store()
        print("Loaded existing ChromaDB successfully.")
    except Exception as e:
        print(f"Failed to load ChromaDB: {e}")
        return

    # 2. Create RAG pipeline
    print("\n[Step 2] Creating RAG Pipeline...")
    qa_chain = create_rag_pipeline(vector_store)

    # 3. Start CLI Query Test
    print("\n[Step 3] CLI Query Test (Using Existing Embeddings Only)")
    print("Enter a query (or 'exit' to quit):")

    while True:
        query = input("Query> ")
        if query.lower() in ["exit", "quit"]:
            break

        try:
            result = qa_chain.invoke({"query": query})
            print(f"Answer: {result['result']}\n")
        except Exception as e:
            print(f"Query error: {e}")

if __name__ == "__main__":
    main()
