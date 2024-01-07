"""Use models locally using HuggingFace API.

The idea is to run the model as a multiprocess in python 
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
from pygitai.context import Context
from pygitai.models.prompt import generate_prompt


def model_inference(prompt: List[str], ctx: Context) -> str:
    
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate
    generate_ids = model.generate(inputs.input_ids, max_length=30)
    commit_output = tokenizer.batch_decode(
        generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]

    return commit_output
