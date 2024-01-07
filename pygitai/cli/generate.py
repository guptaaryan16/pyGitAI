import click
from typing import Any


@click.command("generate")
@click.option(
    "--include-body",
    is_flag=True,
    default=False,
    help="generate a title and body for the branch",
)
@click.option(
    "--body-length", type=int, default=200, required=False, help="PR body length"
)
@click.option(
    "--ref-branch",
    type=str,
    default="main",
    help="default reference branch to generate commit",
)
@click.option("--PR-authors", type=list[str], help="list PR author names to add in the message")
@click.help_option("--help", "-h", help="show the `pygit generate` help page")
def generate(
    include_body: bool, 
    body_length: int, 
    ref_branch: str, 
    PR_authors: Any
    ):
    """Generate PR changes along with title and body for merge with repos(for small issues)
    
    The idea is to to take a complete branch and generate a title and a message for all the changes happened in the PR. This can also include fetching the issue details on github using octokit API and using it to craft a perfect PR on the upstream branch.
    """



    return NotImplementedError
