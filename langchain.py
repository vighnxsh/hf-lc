import os
import urllib3
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from langchain.llms.base import LLM
from typing import Any, List, Optional

class CustomHuggingFaceInference(LLM):
    client: Any
    
    def __init__(self, client):
        super().__init__()
        self.client = client

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.text_generation(prompt, max_new_tokens=500)
        return response

    @property
    def _llm_type(self) -> str:
        return "custom_huggingface_inference"



load_dotenv()

hf_token = os.getenv("HUGGINGFACE_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")

inference_client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=hf_token,
)

llm = CustomHuggingFaceInference(client=inference_client)

question = "Who won cricket world cup in year 2011?"
template = """Question: {question}\nAnswer: Let's think step by step"""
prompt = PromptTemplate(template=template, input_variables=["question"])
print(prompt)

chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run(question))