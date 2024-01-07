"""
The main file to handle prompts for `pygit.cli.commit` command.

# Reference from https://github.com/Nutlope/aicommits/blob/develop/src/utils/prompt.ts#L20C2-L34C5

"""

from pygitai.context import Context
from pygitai.git import get_staged_diff

commit_type_formats: [str, str] = {
    "": "<commit message>",
    "conventional": "<type>(<optional scope>): <commit message>",
}


def specify_commit_format(commit_type: str) -> str:
    return f"The output response must be in format:\n{commit_type_formats[commit_type]}"


commit_types: [str, str] = {
    "": "",
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


def generate_prompt(
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
        specify_commit_format(commit_type),
        get_staged_diff(ctx).__str__(),
        f"Message language: {locale}",
        f"Commit message must be a maximum of {max_length} characters.",
        "Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commit.",
    ]

    if include_body:
        prompt_message.append(
            f"Add a body after the first line of length {ctx.body_length} that summerize the changes added to the repository."
        )
    return "\n".join(filter(None, prompt_message))
