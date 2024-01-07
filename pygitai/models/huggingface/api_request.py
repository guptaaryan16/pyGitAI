import requests
import json
from pygitai.context import Context
from .models_dict import HF_models_dict
import re


def fetch_message_from_hf(ctx: Context, prompt: str):
    """Fetch the message from HF model using Inference API.

    For more information about the model and the inference API, you can read https://huggingface.co/inference-api.
    """

    payload = {"inputs": prompt, "parameters": {"return_full_text": False}}
    headers = {"Authorization": f"Bearer {ctx.model_prop['auth_token']}"}
    API_URL = HF_models_dict[ctx.model_prop["model"]]["API_KEY_LINK"]

    # Make a request to the inference API url
    response = requests.post(API_URL, headers=headers, json=payload)

    commit_title, commit_body = _clean_hf_response(
        response.json()[0]["generated_text"], include_body=ctx.include_body
    )

    return commit_title, commit_body


def _clean_hf_response(content: str, include_body: str = False) -> str:
    """Clean the raw output from the HF LLMs."""
    content = content.split("\n")

    generated_content = []

    for text in content:
        if text != "" and "<" not in text and text not in generated_content:
            generated_content.append(text)

    commit_title = generated_content[0]
    commit_body = ""

    if include_body:
        generated_content = generated_content[1:]
        print(generated_content)
        commit_body = " ".join(generated_content)

    return commit_title, commit_body
