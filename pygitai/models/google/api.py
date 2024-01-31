# The file to generate commit messages for the calls made to OpenAI models
# Based on https://platform.openai.com/docs/guides/text-generation/chat-completions-api

import os
from pygitai.context import Context


def fetch_message_google_client(
    ctx: Context,
    prompt: str,
) -> str:
    """Use information Google Vertex Inference End points.

    For more refer https://ai.google.dev/tutorials/python_quickstart. The google docs 
    provides great guide on usage of the APIs and their models requirements.
    """
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            """Using google models require installing `google-generativeai` package like this `pip install -q -U google-generativeai`."""
        )

    genai.configure(api_key=ctx.model_prop["api_key"])

    try:
        model = genai.GenerativeModel(ctx.model_prop["model"])
        response = model.generate_content(prompt)

    except ConnectionError:
        raise ConnectionError(
            "Google-generative Client raises connection error. Please check the API key and endpoints."
        )

    return response["choices"][0]["message"]["content"]