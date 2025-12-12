from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chroma_setup import get_chroma_vector_store
from langchain_pipeline import create_rag_pipeline
import os

app = Flask(__name__)
CORS(app)

# Global variables for the pipeline
qa_chain = None

def initialize_chatbot():
    global qa_chain
    try:
        print("Initializing Vector Store...")
        vector_store = get_chroma_vector_store()
        print("Vector Store Loaded. Creating RAG Pipeline...")
        qa_chain = create_rag_pipeline(vector_store)
        print("Chatbot Initialized Successfully.")
    except Exception as e:
        print(f"Error initializing chatbot: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global qa_chain
    if not qa_chain:
         return jsonify({"error": "Chatbot not initialized"}), 500
    
    data = request.json
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        response = qa_chain.invoke({"query": user_query})
        return jsonify({"result": response['result']})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    initialize_chatbot()
    print("Starting Flask Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
