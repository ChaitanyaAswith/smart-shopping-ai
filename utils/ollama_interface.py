import requests

# Set the URL for your Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"  # Adjust this URL if needed

def query_ollama(prompt: str, model: str = "llama3") -> str:
    """
    Queries the Ollama model using a given prompt and model name.
    
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use (default is "llama3").
    
    Returns:
        str: The response from the model.
    """
    payload = {
        "model": model,  # Specify the model you want to use (e.g., "llama3")
        "prompt": prompt,
        "stream": False  # Set stream to False for a full response
    }

    try:
        # Send the request to Ollama's API
        response = requests.post(OLLAMA_URL, json=payload)
        # Raise an exception if the response status code is not 200
        response.raise_for_status()
        # Parse the response JSON and return the 'response' field
        return response.json().get("response", "").strip()
    
    except requests.exceptions.RequestException as e:
        # In case of any exception, return an error message
        return f"Error contacting Ollama: {e}"
