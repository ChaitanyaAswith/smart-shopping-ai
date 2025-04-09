from utils.ollama_interface import query_ollama

# Simple test prompt
prompt = "Hello, what is the weather like today?"

# Use the default model (llama3) to query Ollama
response = query_ollama(prompt, model="llama3")

print(f"Response from Ollama: {response}")
