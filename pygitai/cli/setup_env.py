import click
import pygitai
from pathlib import Path
from configparser import ConfigParser
from pygitai.cli.utils import save_setup_config
from pygitai.models.openai import openAI_GPT_setup
import subprocess


types_of_infra_available = ["google-API", "openai-GPT-3.5", "HuggingFace-GPT2"]


def HuggingFaceModel_setup(setup_config: ConfigParser) -> Exception:
    """Main function for setup of HuggingFace models calls"""
    click.echo(
        "Not supported as of now. Please consider contributing to the project to use this feature."
    )
    return NotImplementedError


def Google_API(setup_config: ConfigParser) -> Exception:
    """Main function for setup of Google API calls"""
    click.echo(
        "Not supported as of now. Please consider contributing to the project to use this feature."
    )
    return NotImplementedError


@click.command()
@click.option(
    "--cache-dir",
    type=Path,
    default="./",
    help="path of pygit_cache for config storage",
)
@click.help_option("-h", "--help", help="the help message for pygit setup")
def setup_environment_config(cache_dir: Path):
    """Setup ENV variables for the model / API keys available."""
    click.echo(
        f"""Welcome to pyGitAI {pygitai.__version__}\nWhich type of model do you want to use here?"""
    )
    for i, c in enumerate(types_of_infra_available):
        click.echo(f"{i+1} {types_of_infra_available[i]}")
    choice = int(input()) - 1

    setup_config = ConfigParser()

    # Now ask the ENV variables for the model and the extension
    match choice:
        case 0:
            local_model_setup(setup_config)
        case 1:
            openAI_GPT_setup(setup_config)
        case 2:
            HuggingFaceModel_setup(setup_config)
        case _:
            click.echo(
                "Please select one of the options or contribute to the project for more choices to be available :-)"
            )

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

    setup_config["git"] = {"author": author, "email": email, "ref-branch": ref_branch}

    # Create config file for the project
    save_setup_config(cache_dir, setup_config=setup_config)