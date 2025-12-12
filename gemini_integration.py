import requests

def query_gemini_api(prompt, api_key):
    """
    Queries the Gemini API with a given prompt.

    Args:
        prompt (str): The input prompt for the LLM.
        api_key (str): The API key for authenticating with the Gemini API.

    Returns:
        str: The response from the Gemini API.
    """
    url = "https://api.gemini.com/v1/llm"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Example usage
    api_key = "your_gemini_api_key"  # Replace with your Gemini API key
    prompt = "What is the capital of France?"
    try:
        response = query_gemini_api(prompt, api_key)
        print("Gemini API Response:", response)
    except Exception as e:
        print("Error:", e)