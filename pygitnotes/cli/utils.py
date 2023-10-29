from configparser import ConfigParser
from pathlib import Path
import os


def _config_exists()->bool:
    '''Check if config files exist or to tell the user to setup the pygit extension'''
    if os.path.isdir('./.pygit_cache') and os.path.isfile('./.pygit_cache/CACHEDIR.TAG'):
        return True 
    return False 
    

def _create_cache_directory()->None:
    # create cache directory in the project for PyGitNotes
    # using standard defined in https://bford.info/cachedir/
    
    if _config_exists():
        return
    else:
        os.makedirs('./.pygit_cache') 

    cache_str = '''Signature: 8a477f597d28d172789f06886806bc55\n# This file is a cache directory tag created by PyGitNotes.\n# For information about cache directory tags, see:\n#	http://www.brynosaurus.com/cachedir/'''

    with open('./.pygit_cache/CACHEDIR.TAG', 'a') as f:
        f.write(cache_str)


def save_setup_config(cache_dir: Path, setup_config: ConfigParser)->None:
    '''the function to create cache and save config files for pygit'''
    
    # Create a cache directory
    _create_cache_directory()
    
    # create a congig file 
    with open('./.pygit_cache/config.ini', 'w') as configfile:
        setup_config.write(configfile)


def load_setup_config()->ConfigParser:
    '''load the setup config or ask for setup if nothing is available in ./pygit_cache '''
    if not _config_exists():
        click.echo('Setup pyGitNotes first with --setup Flag')
    
    config = ConfigParser()
    return config.read('./.pygit_cache/config.ini')