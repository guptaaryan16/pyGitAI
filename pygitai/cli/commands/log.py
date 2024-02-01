import click
from typing import Any
import subprocess


@click.command("log")
@click.argument("log_args", nargs=-1)
@click.help_option("-h", "help")
def log(log_args: Any):
    """Git log extended to pygit."""

    command = ["git", "log"]

    # Prepare the ls command with the provided options
    for log_arg in log_args:
        if len(log_arg) == 1:
            command.append(["-" + log_arg])
        else:
            command.append(
                ["--" + log_arg]
            )  # Can still show bugs for single arguments, lets see what I do

    # Run the ls command
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of ls command
    click.echo(result.stdout)
