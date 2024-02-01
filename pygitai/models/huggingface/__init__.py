from .models_dict import hf_models_dict
from .setup import hf_inference_setup
from .api_request import fetch_message_from_hf_inference_api
from .local_model import local_model_inference
from pygitai.context import Context
from typing import Any


__all__ = ["hf_models_dict", "hf_inference_setup", "hf_inference_function"]


def hf_inference_function(
    ctx: Context, prompt: str, command_type: str = "commit"
) -> Any:
    """Inference Function to control the inputs and outputs depending on `pygit` commands.

    The inference function chooses the necessary abstraction for the use of the model over the current HF inference API endpoints. This allows you to remove necessary content and make sure the output matches the format as desired by the user.
    """
    match command_type:
        case "commit":
            return hf_fetch_and_clean_response_commit(ctx, prompt)
        case "generate-pr":
            return hf_generate_pr_comment(ctx, prompt)
        case "comment":
            return hf_generate_code_comment(ctx, prompt)
        case _:
            return fetch_message_from_hf_inference_api(ctx, prompt)


def hf_fetch_and_clean_response_commit(ctx: Context, prompt: str) -> Any:
    """Fetch the commit title and body using correct HF model.

    The function selects the HF method used for inference of the prompt, i.e.
    either HF inference API or the local custom model and tokenizer and use that to
    generate the appropriate response to the prompt for the commit generation.
    """
    response = fetch_message_from_hf_inference_api(ctx, prompt)

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


def hf_generate_pr_comment(ctx: Context, prompt: str) -> Any:
    """Generate a PR Title and Comment for the Git Feature Branch

    The function allows you to choose and make request to the correct API endpoint and thus,
    helps in making the necessary changes in the HF inference API output.
    """
    response = fetch_message_from_hf_inference_api(ctx, prompt)
    return response


def hf_generate_code_comment(ctx: Context, prompt: str) -> str:
    """Fetch the code commented diff using correct HF model.

    The function selects the HF method used for inference of the prompt, i.e.
    either HF inference API or the local custom model and tokenizer and use that to
    generate the appropriate response to the prompt for the commit generation.
    """
    response = fetch_message_from_hf_inference_api(ctx, prompt)

    # Clean the HF generated diff patch as per the problems in the API generation

    # Specific formatting issues to be removed, so that the function is ready for diff preview.
    diff_patch = "".join(response.split("```"))
    diff_patch = "\n".join(diff_patch.split("\n"))[2:]

    return diff_patch
