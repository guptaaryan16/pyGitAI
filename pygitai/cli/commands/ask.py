import click
from typing import Any


@click.command("ask")
@click.help_option("-h", "help")
def ask():
    """Git log extended to pygit. May use it for something better in future ;-)"""
    pass
