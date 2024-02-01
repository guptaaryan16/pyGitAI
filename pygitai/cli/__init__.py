import pygitai
import click
from pygitai.cli.commands import (
    commit,
    generate,
    log,
    comment
)
from pygitai.cli.setup import setup_environment_config


@click.group()
@click.version_option(pygitai.__version__, "--version", "-v", prog_name="pyGitAI")
@click.help_option("--help", "-h", help="help message for pyGitAI")
def main():
    """Entry point of pyGitAI commands"""
    pass


# The commands for pygit CLI interface
main.add_command(setup_environment_config, "setup")
main.add_command(commit, "commit")
main.add_command(comment, "comment")
main.add_command(generate, "generate-pr")
main.add_command(log, "log")

__all__ = [
    "main",
    "setup_environment_config",
    "commit",
    "comment",
    "generate",
    "log"
]
