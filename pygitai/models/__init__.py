from pygitai.context import Context
from pygitai.models.openai import (
    openai_inference_function,
    openai_models_dict,
    openai_gpt_setup,
)
from pygitai.models.huggingface import (
    hf_inference_function,
    hf_inference_setup,
    hf_models_dict,
)
from typing import Any
from pygitai.models.google import (
    google_inference_function,
    google_models_dict,
    google_inference_setup,
)

__all__ = [
    "hf_inference_setup",
    "google_inference_setup",
    "openai_gpt_setup",
    "generate_commit_message",
    "generate_pr_prompt",
    "generate_code_comment",
]


def _choose_backend_inference_function(
    ctx: Context, prompt: str, command_type: str
) -> Any:
    # The idea is to select the model from the ctx and use the prompt to access
    match ctx.model_source:
        case "openAI":
            return openai_inference_function(ctx, prompt, command_type)

        case "HF":
            return hf_inference_function(ctx, prompt, command_type)

        case "Google-API":
            return google_inference_function(ctx, prompt, command_type)


def generate_commit_message(ctx: Context, prompt: str) -> Any:
    """Select the LLM and pass the git diff prompt to the model to generate commit message."""

    commit_message, commit_body = _choose_backend_inference_function(
        ctx, prompt, "commit"
    )
    return commit_message, commit_body


def generate_pr_prompt(ctx: Context, prompt: str):
    """Select the correct API interface and request PR Title and Body."""

    pr_title, pr_body = _choose_backend_inference_function(ctx, prompt, "comment-pr")
    return pr_title, pr_body


def generate_code_comment(ctx: Context, prompt: str) -> str:
    """Select the LLM and pass the git prompt to the model."""

    function_diff = _choose_backend_inference_function(ctx, prompt, "")
    
    return function_diff
