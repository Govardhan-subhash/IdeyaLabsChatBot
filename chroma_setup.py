import chromadb
from chromadb.config import Settings

def setup_chroma_db():
    """
    Sets up the Chroma vector database.

    Returns:
        chromadb.Client: A Chroma database client instance.
    """
    client = chromadb.Client(Settings(
        persist_directory="./chroma_db",  # Directory to store the database
        chroma_db_impl="duckdb+parquet",  # Database implementation
        anonymized_telemetry=False
    ))
    return client

def add_to_chroma_db(client, collection_name, documents, metadatas):
    """
    Adds documents to a Chroma collection.

    Args:
        client (chromadb.Client): The Chroma database client.
        collection_name (str): Name of the collection.
        documents (list): List of document texts.
        metadatas (list): List of metadata dictionaries corresponding to the documents.
    """
    collection = client.get_or_create_collection(name=collection_name)
    collection.add(documents=documents, metadatas=metadatas)

def query_chroma_db(client, collection_name, query_text, n_results=5):
    """
    Queries the Chroma database for similar documents.

    Args:
        client (chromadb.Client): The Chroma database client.
        collection_name (str): Name of the collection to query.
        query_text (str): The query text.
        n_results (int): Number of results to return.

    Returns:
        list: List of results from the query.
    """
    collection = client.get_collection(name=collection_name)
    results = collection.query(query_texts=[query_text], n_results=n_results)
    return results

if __name__ == "__main__":
    # Example usage
    client = setup_chroma_db()
    documents = ["This is a sample document.", "Another example document."]
    metadatas = [{"source": "example1"}, {"source": "example2"}]
    add_to_chroma_db(client, "example_collection", documents, metadatas)

    query_results = query_chroma_db(client, "example_collection", "sample")
    print("Query Results:", query_results)