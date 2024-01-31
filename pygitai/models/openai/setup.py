import click
from .models_dict import openai_models_dict
from configparser import ConfigParser


def openai_gpt_setup(setup_config: ConfigParser):
    """Main function for setup of OpenAI-GPT model calls"""

    click.echo(
        """Welcome to OpenAI APIs setup to use pyGitAI\nNow enter your credentials and API keys\n(dont't worry they will be encrypted and stored locally on the computer :-| ): """
    )
    API_KEY = input("API Key:")

    click.echo("Choose the model for inference: ")
    for i, model in enumerate(openai_models_dict):
        click.echo(f"{i+1}. {model}")
    model_id = int(input()) - 1
    model = openai_models_dict[model_id]

    click.echo("Should we keep this as a default option? (y/n) (y): ")
    option = input()

    if option != "n":
        # Add as the default use case for the project
        setup_config["default"] = {"default_platform": "OpenAI"}

    # Setting Up config
    setup_config["OpenAI"] = {"API_KEY": API_KEY, "model": model}
