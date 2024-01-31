import requests
import json
from pygitai.context import Context
from .models_dict import hf_models_dict
import re


def fetch_message_from_hf_inference_api(ctx: Context, prompt: str):
    """Fetch the message from HF model using Inference API.

    For more information about the model and the inference API, you can read https://huggingface.co/inference-api.
    """
    payload = {"inputs": prompt, "parameters": {"return_full_text": False}}

    headers = {"Authorization": f"Bearer {ctx.model_prop['auth_token']}"}
    API_URL = hf_models_dict[ctx.model_prop["model"]]["API_KEY_LINK"]

    # Make a request to the inference API url
    response = requests.post(API_URL, headers=headers, json=payload)
    
    return response.json()[0]["generated_text"]
