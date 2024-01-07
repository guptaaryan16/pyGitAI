import click
import subprocess
import git
from pathlib import Path
from pygitai.context import Context
from pygitai.exceptions import (
    NoGPTResponseError,
    NotAGitRepositoryError,
    CommandFailure,
)
from pygitai.cli.utils import (
    load_setup_config,
    clean_subprocess_output,
)
from pygitai.git import get_staged_diff
from pygitai.models import generate_commit_message, generate_prompt


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
):
    """Custom Git Commit Command to work with LLM models."""

    # prepare the git command with custom options
    try:
        repo = git.Repo("./")
    except git.exc.InvalidGitRepositoryError:
        raise NotAGitRepositoryError(
            "Please run `git init` or use a valid git repository"
        )

    # Load the setup_env config
    config = load_setup_config()

    # check for the -gm and -m '<message>' flags if they exist together
    if generate_message and message != "":
        raise ValueError(
            "Option to generate message and message argument cannot be used together"
        )

    # invoke git context function
    ctx = Context(config, repo)

    if from_commit:
        # Update the previous commit
        ctx.last_commit = from_commit

    if include_body:
        # include body in the commit
        ctx.include_body = True
        ctx.body_length = body_length

    git_command = ctx.git_stack = ["git", "commit", "-m"] 

    if generate_message:
        try:
            # Call the subprocess to generate the git commit message
            commit_message, commit_body = generate_commit_message(ctx)
            if include_body:
                message = commit_message + '\n\n' + commit_body
            else:
                message = commit_message
        except ChildProcessError:
            raise NoGPTResponseError("pygit-commit failed to generate message.")

    if editable:
        message = click.edit(text=message, editor=editor)

    git_command.append(message)

    try:
        output = subprocess.run(git_command)
        click.echo(clean_subprocess_output(output))

    except subprocess.CalledProcessError:
        raise CommandFailure(
            "pygit-commit run failed. Report the issue to the developer :-("
        )

