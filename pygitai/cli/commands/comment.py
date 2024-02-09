import click
import subprocess
import inspect
import os
import sys

from typing import Any
from pathlib import Path

from pygitai.cli.utils import check_and_setup_command_env_ctx
from pygitai.models import generate_code_comment
from pygitai.git import (
    get_git_revert_diff_content,
    save_git_patch_in_cache,
    apply_git_revert_patch,
)
from pygitai.exceptions import (
    NoGPTResponseError,
    NotAGitRepositoryError,
    CommandFailure
)


def get_function_signature_and_code(module_name, function_name, path=None):
    """Fetch the function name and source code for passing on to LLM Model."""
    try:
        if path:
            absolute_path = os.path.abspath(path)
            module_name = os.path.splitext(os.path.basename(absolute_path))[0]
            # Load the module dynamically
            # Based on https://github.com/epfl-scitas/spack/blob/af6a3556c4c861148b8e1adc2637685932f4b08a/lib/spack/llnl/util/lang.py#L595-L622
            if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
                import importlib.util

                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

            elif sys.version_info[0] == 3 and sys.version_info[1] < 5:
                import importlib.machinery

                loader = importlib.machinery.SourceFileLoader(module_name, path)
                module = loader.load_module()

        else:
            import importlib

            module = importlib.import_module(module_name)

        _function = getattr(module, function_name)
        signature = inspect.signature(_function)
        source_code = inspect.getsource(_function)
        return signature, source_code

    except (ImportError, AttributeError):
        click.echo(
            f"Error: Function '{function_name}' not found in module '{module_name}'"
        )
        return None, None


def generate_comment_prompt(source_code: str, docstring_format="Numpy") -> str:
    """Generate prompt message for the function name entered by the user in the file."""
    prompt_message = [
        f"Generate docstrings in {docstring_format} format for the following function code:",
        f"\n{source_code}\n",
        "Please only add docstrings in function code as output with comments and do not do any changes in the source code. Start the output with the function signature directly without code brackets ``````",
    ]
    return "\n".join(prompt_message)


@click.command("comment")
@click.option(
    "--module",
    default="__main__",
    type=str,
    help="Specify the module containing the function",
)
@click.option(
    "--path",
    default=None,
    type=str,
    help="Specify the path of the function with respect to root directory",
)
@click.option(
    "--function-name", type=str, help="Specify the function you want to create docstrings for"
)
@click.option(
    "--docstring-format",
    type=click.Choice(["Numpy", "Google"]),
)
@click.option(
    "--revert",
    type=bool,
    default=False,
    help="Revert the function docstrings generated earlier due to some errors.",
)
@click.help_option("-h", "help", help="Generate documentation for the command.")
def comment(
    module: str,
    path: str,
    function_name: str,
    docstring_format: str,
    revert: bool,
):
    """Comment a function by providing its signature using LLM"""

    # Load the context for the command
    ctx = check_and_setup_command_env_ctx()

    if not revert:
        module_name = module or "__main__"
        _, function_code = get_function_signature_and_code(
            module_name, function_name, path
        )

        with open(path, "r") as patch_file:
            source_code = patch_file.read()

        if function_code:
            try:
                # Call the subprocess to generate the git commit message
                prompt = generate_comment_prompt(function_code, docstring_format)
                diff_patch = generate_code_comment(ctx, prompt)
            except ChildProcessError:
                raise NoGPTResponseError(
                    "pygit-comment failed to generate Doc-Strings."
                )
            # Apply comments to the original code
            git_diff_patch = get_git_revert_diff_content(
                source_code, function_code, diff_patch, path
            )

            # Save git Diff patch to allow reverts directly with the command
            # Save method also register change according to branch in .pygit_cache/comment/<branch>
            save_git_patch_in_cache(ctx, git_diff_patch, path)

    else:
        # Load and apply reverted changed
        # Revert deletes changes made in .pygit_cache/comment/<branch>
        apply_git_revert_patch(ctx, path)
