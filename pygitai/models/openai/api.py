# The file to generate commit messages for the calls made to OpenAI models
# Based on https://platform.openai.com/docs/guides/text-generation/chat-completions-api

import os
from pygitai.context import Context
from typing import Any


def fetch_message_openai(
    ctx: Context,
    prompt: str,
) -> Any:
    try:
        from openai import OpenAI, OpenAIError
    except ImportError:
        raise ImportError("Using OpenAI requires installing OpenAI Client for python")

    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model=ctx.model_prop["model"],
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant. You will write helpful commit messages and code based on the prompt and information provided."
                },
                {  
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

    except OpenAIError as e:
        raise OpenAIError(f"OpenAI Client raises error: {e}.")

    return response["choices"][0]["message"]["content"]
