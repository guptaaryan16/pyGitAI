import click
from .models_dict import HF_models_dict
from configparser import ConfigParser


def HF_inference_setup(setup_config: ConfigParser):
    """Main function for setup of HF model inference API calls"""

    click.echo(
        """Welcome to Huggingface Inference API setup to use pyGitAI\nNow enter your credentials and API keys\n(dont't worry they will be encrypted and stored locally on the computer :-| ): """
    )

    AUTH_TOKEN = input("AUTH TOKEN:")
    HF_models_availabe = list(HF_models_dict.keys())

    click.echo("Choose the model for inference: ")
    for i, model in enumerate(HF_models_availabe):
        click.echo(f"{i+1}. {model}")
    model_id = int(input()) - 1

    model = HF_models_availabe[model_id]
    
    click.echo("Should we keep this as a default option? (y/n) (y): ")
    option = input()

    if option != "n":
        # Add as the default use case for the project
        setup_config["default"] = {"default_platform": "HF"}

    # Setting Up config
    setup_config["HF"] = {"AUTH_TOKEN": AUTH_TOKEN, "model": model}
