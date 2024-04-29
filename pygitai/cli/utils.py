from configparser import ConfigParser
from pathlib import Path
import os
from git import Repo
from pygitai.context import Context
from pygitai.exceptions import NotValidConfig


def _config_dir_exists(cache_dir: str = "./.pygit_cache") -> bool:
    """Check if config files exist or to tell the user to setup the pygit extension"""
    return os.path.isdir(cache_dir) and os.path.isfile(f"{cache_dir}/CACHEDIR.TAG")


def _config_exist_and_valid(cache_dir: str = "./.pygit_cache") -> bool:
    """Check if the Config.ini file exists and is valid for making an LLM request."""
    return _config_dir_exists(cache_dir) and os.path.isfile("./.pygit_cache/config.ini")


def _create_cache_directory(cache_dir: str = "./.pygit_cache") -> None:
    """Create cache directory in the project for PyGitAI

    This is done using the standard defined in https://bford.info/cachedir/ ."""
    if _config_dir_exists(cache_dir):
        return
    else:
        os.makedirs(cache_dir)

    cache_str = """Signature: 8a477f597d28d172789f06886806bc55\n# This file is a cache directory tag created by pyGitAI.\n# For information about cache directory tags, see:\n#	http://www.brynosaurus.com/cachedir/"""

    with open(cache_dir + "/CACHEDIR.TAG", "a") as f:
        f.write(cache_str)


def save_setup_config(setup_config: ConfigParser, cache_dir: str = "./.pygit_cache") -> None:
    """Function to create cache and save config files for pygit"""

    # Create a cache directory
    _create_cache_directory(cache_dir)

    # Clear the conig.ini file
    os.remove('./.pygit_cache/config.ini')

    # create a congig file
    with open("./.pygit_cache/config.ini", "w") as configfile:
        setup_config.write(configfile)


def _load_setup_config(cache_dir: str = "./.pygit_cache") -> ConfigParser:
    """Load the setup config or ask for setup if nothing is available in ./pygit_cache"""
    if not _config_exist_and_valid():
        raise NotValidConfig("Setup pyGitAI first with `pygit setup`")

    config = ConfigParser()
    config.read(f"{cache_dir}/config.ini")
    return config


def check_and_setup_command_env_ctx()-> Context:
    """Setup and return basic environment Context variable to be used by commands."""
    try:
        repo = Repo("./")
    except git.exc.InvalidGitRepositoryError:
        raise NotAGitRepositoryError(
            "Please run `git init` or use a valid git repository"
        )

    # Load the setup_env config
    config = _load_setup_config()

    # Setting up context
    ctx = Context(config, repo)

    return ctx


def clean_subprocess_output(output: str) -> str:
    lines = output.__str__().split("\n")[:-1]

    # Join the lines back together
    return "\n".join(lines)
