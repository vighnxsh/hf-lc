import os
import urllib3
from huggingface_hub import InferenceClient

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


os.environ['CURL_CA_BUNDLE'] = ""

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
 
  
)

response = client.text_generation("What is machine learning?")
print(response)