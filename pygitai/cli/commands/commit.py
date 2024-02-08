import os
import click
import subprocess
from pathlib import Path

from pygitai.exceptions import (
    NoGPTResponseError,
    NotAGitRepositoryError,
    CommandFailure
)
from pygitai.cli.utils import check_and_setup_command_env_ctx, clean_subprocess_output
from pygitai.git import get_staged_diff, delete_git_saved_patches
from pygitai.models import generate_commit_message
from pygitai.context import Context


commit_type_formats: [str, str] = {
    "normal": "```<commit message>```",
    "conventional": "```<type>(<optional scope>): <commit message>```",
}

commit_types: [str, str] = {
    "normal": "",
    "conventional": """
    Choose a type from the type-to-description dictionary below that best describes the git diff:
        {
        "docs": "Documentation only changes",
        "style": "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
        "refactor": "A code change that neither fixes a bug nor adds a feature",
        "perf": "A code change that improves performance",
        "test": "Adding missing tests or correcting existing tests",
        "build": "Changes that affect the build system or external dependencies",
        "ci": "Changes to our CI configuration files and scripts",
        "chore": "Other changes that don't modify src or test files",
        "revert": "Reverts a previous commit",
        "feat": "A new feature",
        "fix": "A bug fix"
        }
        """,
}


def generate_commit_prompt(
    ctx: Context,
    locale: str = "en-US",
    include_body: bool = False,
    max_length: int = 150,
    commit_type: str = "",
) -> str:
    # The call is made to a LLM model to get the data from the files
    prompt_message = [
        "Generate a concise git commit message written in present tense for the following code diff with the given specifications below:",
        commit_types[commit_type],
        f"Message language: {locale}",
        f"Commit message must be a maximum of {max_length} characters.",
        "Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commit.",
    ]

    # Genertaing Git Diff for the files and adding it to prompt
    prompt_message.append(
        get_staged_diff(ctx),
    )

    if include_body:
        prompt_message.append(
            f"Add a body after the first line of length {ctx.body_length} that summerize the changes added to the repository."
        )

    prompt_message.append(
        f"The first line should be only a commit message of the format {commit_type_formats[commit_type]}, whithout any other description. The commit message is : "
    )

    return "\n".join(filter(None, prompt_message))


PYGIT_COMMIT_UNSAFE_BEHAVIOUR = os.getenv("PYGIT_COMMIT_UNSAFE_BEHAVIOUR")


@click.command("commit")
@click.option(
    "-m",
    "--message",
    type=str,
    default="",
    required=False,
    help="the commit message for manual commit",
)
@click.option(
    "--generate-message",
    "-gm",
    is_flag=True,
    help="to generate commit message by LLM model",
)
@click.option(
    "--from-commit",
    "-fc",
    required=False,
    type=str,
    default="^HEAD",
    help="Last commit hash from which summary is generated",
)
@click.option(
    "--repo-path",
    type=Path,
    required=False,
    default=Path("./"),
    help="path to git repo",
)
@click.option(
    "--include-body",
    is_flag=True,
    required=False,
    help="Generate a body along with the commit",
)
@click.option(
    "--body-length",
    "-bl",
    type=int,
    default=200,
    required=False,
    help="Length of body text that needs to be generated",
)
@click.option(
    "--editable",
    "-e",
    is_flag=True,
    help="Edit the commit message in editor before it is commited",
)
@click.option(
    "--editor",
    type=click.Choice(["vim", "nano"]),
    default="vim",
    help="Choose editor: vim or nano",
)
@click.option(
    "--commit_type",
    type=click.Choice(["normal", "conventional"]),
    default="conventional",
    help="Choose between normal and conventional styles of commit types",
)
@click.help_option("--help", "-h", help="show the `pygit commit` help page")
def commit(
    message: str,
    generate_message: bool,
    from_commit: str,
    repo_path: str,
    include_body: bool,
    body_length: int,
    editable: bool,
    editor: str,
    commit_type: str,
):
    """Custom Git Commit Command to work with LLM models."""

    # check for the -gm and -m '<message>' flags if they exist together
    if generate_message and message != "":
        raise ValueError(
            "Option to generate message and message argument cannot be used together"
        )

    # Load the context for the command
    ctx = check_and_setup_command_env_ctx()

    if from_commit:
        # Update the previous commit
        ctx.last_commit = from_commit

    if include_body:
        # include body in the commit
        ctx.include_body = True
        ctx.body_length = body_length

    ctx.git_stack = ["git", "commit", "-m"]

    if generate_message:
        try:
            # Call the subprocess to generate the git commit message
            prompt = generate_commit_prompt(ctx, commit_type=commit_type)
            commit_message, commit_body = generate_commit_message(ctx, prompt)
            if include_body:
                message = commit_message + "\n\n" + commit_body
            else:
                message = commit_message
        except ChildProcessError:
            raise NoGPTResponseError("pygit-commit failed to generate message.")

    # Allow the messages generated by LLM to be edited
    if editable:
        try:
            message = click.edit(text=message, editor=editor)
        except TypeError:
            raise TypeError(
                "Please use the command again and exit the Vim editor with `:wq`"
            )

    ctx.git_stack.append(message)

    try:
        click.echo(
            subprocess.run(
                ctx.git_stack, check=True, text=True, stdout=subprocess.PIPE
            ).stdout
        )

        if not PYGIT_COMMIT_UNSAFE_BEHAVIOUR:
            delete_git_saved_patches(ctx)

    except subprocess.CalledProcessError:
        raise CommandFailure(
            "pygit-commit run failed. Report the issue to the developer :-("
        )
