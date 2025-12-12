from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def create_langchain_pipeline(chroma_client, collection_name):
    """
    Creates a LangChain pipeline for Retrieval-Augmented Generation (RAG).

    Args:
        chroma_client: The Chroma database client.
        collection_name (str): Name of the Chroma collection to use.

    Returns:
        RetrievalQA: A LangChain RetrievalQA pipeline.
    """
    # Initialize the Chroma vector store
    vector_store = Chroma(
        client=chroma_client,
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings()
    )

    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Use the following context to answer the question accurately:
        Context: {context}
        Question: {question}
        Answer:
        """
    )

    # Create the RetrievalQA pipeline
    qa_pipeline = RetrievalQA(
        retriever=vector_store.as_retriever(),
        prompt=prompt_template
    )

    return qa_pipeline

if __name__ == "__main__":
    from chroma_setup import setup_chroma_db

    # Example usage
    chroma_client = setup_chroma_db()
    collection_name = "example_collection"

    # Create the LangChain pipeline
    qa_pipeline = create_langchain_pipeline(chroma_client, collection_name)

    # Example query
    question = "What is a sample document?"
    response = qa_pipeline.run(question=question)
    print("Response:", response)