import click
from typing import Any
import subprocess
from pathlib import Path
from pygitai.exceptions import (
    NoGPTResponseError,
    NotAGitRepositoryError,
    CommandFailure,
)
from pygitai.cli.utils import check_and_setup_command_env_ctx, clean_subprocess_output
from pygitai.git import get_branch_diff
from pygitai.context import Context
from pygitai.models import generate_pr_message


pr_title_formats: [str, str] = {
    "": "<PR title>",
    "conventional": "[type]: <PR title>",
}


def specify_pr_format(pr_type: str) -> str:
    return f"The output response must be in format:\n{pr_title_formats[pr_type]}"


pr_types: [str, str] = {
    "": "",
    "conventional": """Choose a type from the type-to-description dictionary below that best describes the PR title:
        {
        "DOCS": "Documentation only changes",
        "REF": "A code change that neither fixes a bug nor adds a feature",
        "PERF": "A code change that improves performance",
        "TEST": "Adding missing tests or correcting existing tests",
        "BUILD": "Changes that affect the build system or external dependencies",
        "CI": "Changes to our CI configuration files and scripts",
        "REVERT": "Reverts a previous commit",
        "FEAT": "A new feature",
        "FIX": "A bug fix"
        }
        """,
}


def generate_pr_prompt(
    ctx: Context,
    locale: str = "en-US",
    include_body: bool = False,
    max_length: int = 200,
    issue_number: int = None,
    pr_type: str = "conventional",
) -> str:
    # The call is made to a LLM model to get the data from the files
    prompt_message = [
        "Generate a concise github PR message written in present tense for the following code diff of the branch with the given specifications below:",
        pr_types.get(pr_type, ""),
        f"Message language: {locale}",
        f"Add issue number fixed in the body {issue_number}",
        "Exclude anything unnecessary such as translation. Your entire response will be passed directly into the Github PR title and body.",
    ]

    # Genertaing Git Diff for the files and adding it to prompt
    prompt_message.append(
        get_branch_diff(ctx),
    )

    if include_body:
        prompt_message.append(
            f"Add a body after the first line of length {ctx.body_length} that summerize the changes added to the repository."
        )
    prompt_message.append(
        f"Add the following values, PR Title, PR body clearly seperated by \n in a python string with a full length less than {max_length} characters"
    )
    

    return "\n".join(filter(None, prompt_message))


@click.command("generate-pr")
@click.option(
    "--body-length", type=int, default=200, required=False, help="PR body length"
)
@click.option(
    "--ref-branch",
    type=str,
    default=None,
    help="default reference branch to generate commit",
)
@click.option(
    "--from-commit",
    type=str,
    default=None,
    help="the commit from which the PR message should be generated",
)
@click.option(
    "--issue-number",
    "-i_n",
    type=int,
    default=None,
    help="default reference branch to generate commit",
)
@click.option(
    "--authors", type=list[str], help="list PR author names to add in the message"
)
@click.option(
    "--pr-type",
    default="conventional",
    type=click.Choice(["", "conventional"]),
    help="list PR author names to add in the message",
)
@click.help_option("--help", "-h", help="show the `pygit generate` help page")
def generate(
    body_length: int,
    ref_branch: str,
    from_commit: str,
    issue_number: int,
    authors: Any,
    pr_type: str = "conventional",
):
    """Generate PR changes along with title and body for merge with repos(for small issues)

    The idea is to to take a complete branch and generate a title and a message for all the changes happened in the PR. This can also include fetching the issue details on github/gitlab using octokit API and using it to craft a perfect PR on the upstream branch.
    As a note, this feature may not support extremely long PRs with large number of commits.
   
    # TODO: Find some way to create a draft PR from github or gitlab using respective CLI and enable/disable this feature accordingly
    """

    # Load the context for the command
    ctx = check_and_setup_command_env_ctx()

    if ctx.git_branch == ctx.ref_branch:
        raise ValueError(
            f"pygit generate only works on git branches that are used as feature branches(excluding the ref branch: {ctx.ref_branch})"
        )

    if ref_branch:
        # Update the previous commit
        ctx.ref_branch = ref_branch

    try:
        # Call the subprocess to generate the git commit message
        prompt = generate_pr_prompt(ctx, pr_type=pr_type, issue_number=issue_number)
        pr_content = generate_pr_message(ctx, prompt)

    except ChildProcessError:
        raise NoGPTResponseError(
            "pygit-generate failed to generate message for the pull request"
        )

    click.echo("The generated message is \n\n")
    click.echo(pr_content)
