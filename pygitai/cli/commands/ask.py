import click
from typing import Any


@click.command("ask")
@click.help_option("-h", "help")
def ask():
    """Scan the codebase and answer questions using LLM knowledge.
    
    My aim is to design something that can provide some intuitive idea to the LLM about the prompt and use it to write code and ask and answer questions. I know LLMs are less capable of reasoning and chain-of-thought, but let's implement something and then see the results for itself.
    """
    return NotImplementedError