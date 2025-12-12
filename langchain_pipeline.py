from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

def create_rag_pipeline(vector_store):
    """
    Creates a RAG pipeline using Gemini and the provided vector store.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    prompt_template = """
You are a helpful and respectful AI assistant.

Use the provided context ONLY when the user's question is about IdeyaLabs.

Rules:
1. If the question is NOT about IdeyaLabs (general greetings or general knowledge questions), answer naturally using your general knowledge.
2. If the question IS about IdeyaLabs and relevant context chunks are available, answer strictly using only those context chunks.
3. If the question IS about IdeyaLabs and no relevant context chunks exist:
   - First check if you already know the correct answer from your own general knowledge.
   - If you know it confidently, provide the answer.
   - If you do NOT know it confidently, respond with: "This information is not yet updated."

Context:
{context}

Question:
{question}

Answer:
"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain