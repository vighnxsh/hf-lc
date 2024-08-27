import os
import urllib3
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API token from environment variable
hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")

# Create an InferenceClient with the token and SSL verification disabled
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=hf_token,
   
)

def generate_response(prompt):
    try:
        # Make a request
        response = client.text_generation(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

# Main loop for CLI interaction
if __name__ == "__main__":
    print("Welcome to the Hugging Face Inference API CLI!")
    print("Type 'quit' or 'exit' to end the program.")
    
    while True:
        user_input = input("\nEnter your prompt: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("Thank you for using the Hugging Face Inference API. Goodbye!")
            break
        
        if user_input:
            print("\nGenerating response...")
            response = generate_response(user_input)
            print(f"\nResponse: {response}")
        else:
            print("Please enter a valid prompt.")