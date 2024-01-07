import pygitai
import click
from pygitai.cli.setup import setup_environment_config
from pygitai.cli.commit import commit
from pygitai.cli.generate import generate
from pygitai.cli.log import log
from pygitai.cli.note import note


@click.group()
@click.version_option(pygitai.__version__, "--version", "-v", prog_name="pyGitAI")
@click.help_option("--help", "-h", help="help message for pyGitAI")
def main():
    """Entry point of pyGitAI commands"""
    pass


# The commands for pygit CLI interface
main.add_command(setup_environment_config, "setup")
main.add_command(commit, "commit")
main.add_command(generate, "generate")
main.add_command(log, "log")
main.add_command(note, "note")

__all__ = ["main"]
