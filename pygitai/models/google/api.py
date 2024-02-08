# The file to generate commit messages for the calls made to OpenAI models
# Based on https://platform.openai.com/docs/guides/text-generation/chat-completions-api

import os
from pygitai.context import Context
import requests


def query_google_api(ctx: Context, prompt: str)-> str:
    headers = {
        "Content-Type": "application/json",
    }
    params = {
        "key": ctx.model_prop["auth_token"],
    }

    json_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    },
                ],
            },
        ],
    }
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{ctx.model_prop['model']}:generateContent",
        params=params,
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise ConnectionError(f'Response raise connection error code {response.status_code}, check your API keys and Internet Connection.') 

def fetch_message_google_client(
    ctx: Context,
    prompt: str,
) -> str:
    """Use information Google Vertex Inference End points.

    For more refer https://ai.google.dev/tutorials/python_quickstart. The google docs provides great guide on usage of the APIs and 
    their models requirements.
    """
    response = query_google_api(ctx, prompt)
    return response
