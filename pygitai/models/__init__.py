from pygitai.context import Context
from pygitai.models.prompt import generate_prompt
from pygitai.models.openai import openai_models_dict, fetch_commit_message_openai
from .prompt import generate_prompt
from pygitai.models.huggingface import fetch_message_from_hf

# from pygitai.models.google import fetch_message_openai

from pygitai.models.huggingface.setup import HF_inference_setup
from pygitai.models.huggingface.models_dict import HF_models_dict
from pygitai.models.openai.setup import openAI_GPT_setup
from pygitai.models.openai.models_dict import openai_models_dict

__all__ = [
    "HF_inference_setup",
    "HF_models_dict",
    "openai_models_dict",
    "openAI_GPT_setup",
    "generate_commit_message",
    "generate_PR_title_body",
    "prompt",
]


def generate_commit_message(ctx: Context, commit_type: str = ""):
    """Select the LLM and pass the git prompt to the model."""

    prompt = generate_prompt(ctx, commit_type=commit_type)

    commit_message = ""

    # The idea is to select the model from the ctx and use the prompt to access
    match ctx.model_source:
        case "openAI":
            try:
                commit_message, commit_body = fetch_commit_message_openai(ctx, prompt)
            except NoGPTResponseError:
                raise NoGPTResponseError(
                    f"OpenAI GPT fetch from {ctx.model_use} failed. Try again or check the Keys and the access to specific models."
                )
        case "HF":
            commit_message, commit_body = fetch_message_from_hf(ctx, prompt)

    # The next step is to clean the LLM output and give the message back
    return commit_message, commit_body
