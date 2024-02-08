import click
import pygitai
from pathlib import Path
from configparser import ConfigParser
from pygitai.cli.utils import (
    save_setup_config,
    _config_exist_and_valid,
    _load_setup_config,
)
from pygitai.models import google_inference_setup, openai_gpt_setup, hf_inference_setup
import subprocess
from pathlib import Path

types_of_infra_available = [
    "Google-Vertex-API",
    "OpenAI-API",
    "HuggingFace-Inference-API",
]


@click.command()
@click.option(
    "--cache-dir",
    type=Path,
    default="./",
    help="path of pygit_cache for config storage"
)
@click.help_option("-h", "--help", help="the help message for pygit setup")
def setup_environment_config(cache_dir: Path):
    """Setup ENV variables for the model / API keys available."""
    click.echo(
        f"""\nWelcome to pyGitAI {pygitai.__version__} !\n\nWhich type of model do you want to use here?"""
    )
    for i, c in enumerate(types_of_infra_available):
        click.echo(f"{i+1} {types_of_infra_available[i]}")
    choice = int(input()) - 1
    if _config_exist_and_valid():
        setup_config = _load_setup_config()
    else:
        setup_config = ConfigParser()

    # Now ask the ENV variables for the model and the extension
    setup_choice = [
        google_inference_setup,
        openai_gpt_setup,
        hf_inference_setup
    ]
    if choice in range(len(setup_choice)):
        setup_choice[choice](setup_config)
    else:
        click.echo("Please select one of the options or contribute to the project for more choices to be available :-)")
        return 

    curr_branch = subprocess.check_output(
        ["git", "branch", "--show-current"], encoding="utf-8"
    )[:-1]

    # The ref branch for the project
    option = input(
        f"Is the current branch ({curr_branch}) ref branch for the project? (y or n) "
    )

    if option == "n":
        ref_branch = input("Enter the Ref branch for the project: ")
    else:
        ref_branch = curr_branch

    # Git Author and Email
    author = subprocess.check_output(
        ["git", "config", "--get", "user.name"], encoding="utf-8"
    )[:-1]
    email = subprocess.check_output(
        ["git", "config", "--get", "user.email"], encoding="utf-8"
    )[:-1]

    option = input(f"Is the current author {author} <{email}>? (y or n) ")

    if option == "n":
        author = input("Enter the current author: ")
        email = input("Enter email: ")

    # Setup the project path
    project_path = "./"

    option = input("Is the current path the root of the project? (./) (y/n)")

    if option == "n":
        project_path = imput("Enter project path: ")

    setup_config["git"] = {
        "author": author,
        "email": email,
        "ref-branch": ref_branch,
        "path": project_path,
    }

    # Create config file for the project
    save_setup_config(setup_config)
