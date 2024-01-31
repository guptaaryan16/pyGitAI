import click
from .models_dict import google_models_dict
from configparser import ConfigParser


def google_inference_setup(setup_config: ConfigParser):
    """Main function for setup of Google API calls"""

    click.echo(
        """Welcome to Google API setup to use pyGitAI\nNow enter your credentials and API keys\n(dont't worry they will be encrypted and stored locally on the computer :-| ): """
    )

    AUTH_TOKEN = input("AUTH TOKEN:")

    click.echo("Choose the model for inference: ")
    for i, model in enumerate(google_models_dict):
        if google_models_dict[model]["access_required"]:
            click.echo(
                f"{i+1}. {model} : ( Model access is required and should be availabe to access by HF Id used here)"
            )
        else:
            click.echo(f"{i+1}. {model}")
    model_id = int(input()) - 1

    model = google_models_dict[model_id]

    click.echo("Should we keep this as a default option? (y/n) (y): ")
    option = input()

    if option != "n":
        # Add as the default use case for the project
        setup_config["default"] = {"default_platform": "GOOGLE"}

    # Setting Up config
    setup_config["GOOGLE"] = {"AUTH_TOKEN": AUTH_TOKEN, "model": model}