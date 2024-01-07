import click
from typing import Any
import subprocess


@click.command("usage")
@click.help_option("-h", "help")
def usage(log_args: Any):
    """List the usage of the LLM calls made by the user using Inference APIs.
    
    Since the LLMs calls to the servers can be expensive, especially the 
    """

    # Prepare the ls command with the provided options
    for log_arg in log_args:
        if len(log_arg) == 1:
            command = ["git", "log"] + ["-" + log_arg]
        else:
            command = ["git", "log"] + [
                "--" + log_arg
            ]  # Can still show bugs for single arguments, lets see what I do

    # Run the ls command
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of ls command
    click.echo(result.stdout)
