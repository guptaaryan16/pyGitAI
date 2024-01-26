"""Use models locally using HuggingFace API.

The idea is to run the model as a multiprocess in python and use the subprocess to get the output. This file and logic will be developed keeping in mind the GIL-lock of python.
"""
from pygitai.context import Context

def local_model_inference(prompt: str) -> str:

    try: 
        from transformers import AutoTokenizer, AutoModelForCausalLM
    except ImportError:
        raise ImportError("Please install transformers >= 1.7.0 for the local model infernence method to be used.")

    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-2-7b-chat-hf", cache_dir="./pygit_cache"
    )
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-2-7b-chat-hf", cache_dir="./pygit_cache"
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate
    generate_ids = model.generate(inputs.input_ids, max_length=30)
    commit_output = tokenizer.batch_decode(
        generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]

    return commit_output