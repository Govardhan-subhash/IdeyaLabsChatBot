from chroma_setup import setup_chroma_db, query_chroma_db
from langchain_pipeline import create_langchain_pipeline
from gemini_integration import query_gemini_api

def main():
    """
    Main function to run the chatbot interface.
    """
    # Set up Chroma database
    chroma_client = setup_chroma_db()
    collection_name = "example_collection"

    # Create LangChain pipeline
    qa_pipeline = create_langchain_pipeline(chroma_client, collection_name)

    # Gemini API key
    api_key = "your_gemini_api_key"  # Replace with your Gemini API key

    print("Welcome to the IdeyaLabs Chatbot! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            # Retrieve context from Chroma
            chroma_results = query_chroma_db(chroma_client, collection_name, user_input)
            context = "\n".join([result["document"] for result in chroma_results["documents"]])

            # Generate response using LangChain and Gemini API
            prompt = qa_pipeline.prompt.format(context=context, question=user_input)
            response = query_gemini_api(prompt, api_key)

            print("Chatbot:", response)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()