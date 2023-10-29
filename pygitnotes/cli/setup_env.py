import click
import pygitnotes
import os
from pathlib import Path
from configparser import ConfigParser
from pygitnotes.cli.utils import save_setup_config
import subprocess


types_of_infra_available = [
    'local',
    'openai-GPT-3.5',
    'HuggingFace-GPT2'
]


def openAI_GPT_setup(setup_config: ConfigParser):
    ''' Main function for setup of OpenAI-GPT model calls '''

    click.echo('''Welcome to OpenAI APIs setup to use PyGitNotes\nNow enter your credentials and API keys\n(dont't worry they will be encrypted and stored locally on the computer ;-) ): ''')
    API_KEY = input("API Key:")
    
    # Model Selection
    models = ['GPT-3.5-Turbo', 'GPT-4']
    
    click.echo('Choose the model for inference: ')
    for i, model in enumerate(models):
        click.echo(f'{i+1}. {model}')
    model_id = int(input()) - 1 
    model = models[model_id]
    
    # Setting Up config
    config = {
        'openAI': {
            'API_KEY' : API_KEY,
            'model': model
        }
    }
    
    # Add as the default use case for the project
    setup_config['default'] ={'default' : 'openAI'}

    # Available UseCases
    setup_config['available'] = config



def HuggingFaceModel_setup(setup_config: ConfigParser):
    ''' Main function for setup of HuggingFace-GPT models' calls '''
    click.echo('Not supported as of now. Please consider contributing to the project to use this feature.')
    return NotImplementedError



def local_model_setup(setup_config: ConfigParser):
    ''' Main function for setup of local model location and path calls '''
    click.echo('Not supported as of now. Please consider contributing to the project to use this feature.')
    return NotImplementedError


@click.command()
@click.option('--cache-dir', type=Path, default='./', help='path of pygit_cache for config storage')
@click.help_option('-h','--help', help='the help message for pygit setup')
def setup_environment_config(cache_dir: Path):
    '''Setup ENV variables for the model / API keys available.'''
    click.echo(f'''Welcome to PyGitNotes {pygitnotes.__version__}\nWhich type of model do you want to use here?''')
    for i, c in enumerate(types_of_infra_available):
        click.echo(f'{i+1} {types_of_infra_available[i]}')
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
            click.echo('Please select one of the options or contribute to the project for more choices to be available :-)')


    # The ref branch for the project
    option = input('Is the current branch ref branch for the project? (y or n)')
    
    if (option == 'n'):
        setup_config['ref-branch'] = subprocess.run(['git', 'branch', '--show-current'])
    
    # Git Author and Email
    author = subprocess.check_output(["git", "config", "--get", "user.name"], encoding='utf-8')
    email = subprocess.check_output(["git", "config", "--get", "user.email"], encoding='utf-8')
    
    option = input(f"Is the current author {author}<{email}>? (y or n): ")
    
    if option == 'n':
        author = input('Enter the current author: ')
        email = input('Enter email: ')

    setup_config['git'] = {
        'author': author,
        'email': email
    }

    # Create config file for the project
    save_setup_config(cache_dir, setup_config=setup_config)
