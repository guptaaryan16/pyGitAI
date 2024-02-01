from .models_dict import google_models_dict
from .setup import google_inference_setup
from .api import fetch_message_google_client

from pygitai.context import Context
from typing import Any


__all__ = ["google_models_dict", "google_inference_setup", "google_inference_function"]


def google_inference_function(
    ctx: Context, prompt: str, command_type: str = "commit"
) -> Any:
    """Inference Function to control the inputs and outputs depending on `pygit` commands.

    The inference function chooses the necessary abstraction for the use of the model over the current Google Vertex inference API endpoints. This allows you to remove necessary content and make sure the output matches the format as desired by the user.
    """
    match command_type:
        case "commit":
            return google_fetch_and_clean_response_commit(ctx, prompt)
        case "generate-pr":
            return google_generate_pr_comment(ctx, prompt)
        case "comment":
            return google_generate_code_comment(ctx, prompt)
        case _:
            return fetch_message_google_client(ctx, prompt)


def google_fetch_and_clean_response_commit(ctx: Context, prompt: str) -> Any:
    """Fetch the commit title and body using a Google Vertex AI model."""
    response = fetch_message_google_client(ctx, prompt)

    content = response.split("\n")
    generated_content = []

    for text in content:
        if text != "" and "<" not in text and text not in generated_content:
            generated_content.append(text)

    commit_title = generated_content[0]
    commit_body = ""

    if ctx.include_body:
        generated_content = generated_content[1:]
        print(generated_content)
        commit_body = " ".join(generated_content)
    return commit_title, commit_body


def google_generate_pr_comment(ctx: Context, prompt: str) -> Any:
    """Generate a PR Title and Comment for the Git Feature Branch using a Google Vertex AI model."""
    response = fetch_message_google_client(ctx, prompt)
    return response


def google_generate_code_comment(ctx: Context, prompt: str) -> str:
    """Fetch the code commented diff using a Google Vertex AI model"""
    response = fetch_message_google_client(ctx, prompt)

    # Specific formatting issues to be removed, so that the function is ready for diff preview.
    diff_patch = "".join(response.split("```"))
    diff_patch = "\n".join(diff_patch.split("\n"))[2:]

    return diff_patch
