import pygitnotes 
import click
import os
from pathlib import Path
from pygitnotes.cli.setup_env import setup_environment_config
from pygitnotes.cli.commit import commit
from pygitnotes.cli.generate import generate
from pygitnotes.cli.log import log_generated_commit

@click.group()
@click.version_option(pygitnotes.__version__, "--version", "-v", prog_name='pyGitNotes')
@click.help_option('--help', '-h', help='the help message for PyGitNotes')
def main():
    '''Entry point of pyGitNotes command'''
    pass

main.add_command(setup_environment_config, 'setup')
main.add_command(commit, 'commit')
main.add_command(generate, 'generate')
main.add_command(log_generated_commit, "ai_log")

__all__ = ['main']