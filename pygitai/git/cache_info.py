"""The pygit_cache file management functions for reverting and storing commands.

This is a safety feature provided by pygitai commands to revert any changes done by the commands during the LLM code generation as the developers take the case where this can be dangerous for the systems.
"""
import os
import json
from pathlib import Path
from pygitai.context import Context
import subprocess
import click
import shutil
from typing import Any



def load_diff_info(repo_path: Path) -> Any:
    diff_info_path = repo_path / ".pygit_cache/comment/comment_diff_cache.json"

    if os.path.exists(diff_info_path):
        try:
            with open(diff_info_path, "r") as file:
                return diff_info_path, json.load(file)
        except json.JSONDecodeError:
            return diff_info_path, {}
    else:
        return diff_info_path, {}


def save_diff_info_file(diff_info_path: str, comment_revert_info: dict) -> None:
    # Save diff info file
    with open(diff_info_path.as_posix(), "w") as diff_info_file:
        json.dump(comment_revert_info, diff_info_file)


def _save_and_register_diff_info(
    comment_revert_info: dict,
    git_diff: str,
    ctx: Context,
    file_path: Path,
    diff_info_path: Path,
):
    # Set the initial variable for the git diff info
    if ctx.git_branch not in comment_revert_info:
        comment_revert_info[ctx.git_branch] = {}

    # Set the initial list for checking the
    if file_path.as_posix() not in comment_revert_info[ctx.git_branch]:
        comment_revert_info[ctx.git_branch][file_path.as_posix()] = []

    # Save the git diff patch file in the correct directory and register the change
    save_diff_patch_path = (
        file_path.parent
        / f"{file_path.name}_{len(comment_revert_info[ctx.git_branch][file_path.as_posix()])}.diff"
    )

    # Register the git_diff file and this helps in making reverts smoothly
    comment_revert_info[ctx.git_branch][file_path.as_posix()].append(
        save_diff_patch_path.as_posix()
    )

    # register the file creation in the git info file
    save_diff_info_file(diff_info_path, comment_revert_info)

    # Save git diff patch in the defined path
    with open(save_diff_patch_path.as_posix(), "w") as file:
        file.write(git_diff)


def save_git_patch_in_cache(ctx: Context, git_diff: str, file_path: str) -> None:
    """Save git patch along with info for reverts.

    The search for saved config works like this: First the `comment_diff_cache.json` is loaded which contains information for each diff and how it is stored for a particular commit. After each commit is made through pygit, the information to remove the pygit_cache file is made and through the hash the stored values for the versions is cleared. This behaviour is not allowed if `PYGIT_COMMIT_UNSAFE_BEHAVIOUR` flag is set untrue, which can be done while passing the command or setting up an env variable.

    Files saved:
        - `.pygit_cache/comment/<git-branch-name>/<relative-path-w.r.t.-root_project>/diff-file`
        - `.pygit_cache/<git-branch-name>/comment_stack.py`
    """

    # Get the repo path
    repo_path = Path(ctx.repo.working_dir)

    # Load diff info file
    diff_info_path, comment_revert_info = load_diff_info(repo_path)

    # Converting the file_path into a pathlib.Path type
    file_path = Path(file_path)

    # Create a save_path variable
    save_diff_patch_path = (
        repo_path / ".pygit_cache/comment" / ctx.git_branch / file_path
    )

    # To remove the .. relative lines
    save_diff_patch_path = save_diff_patch_path.absolute().relative_to(
        repo_path.absolute()
    )

    if not save_diff_patch_path.exists():
        save_diff_patch_path.mkdir(parents=True)

    _save_and_register_diff_info(
        comment_revert_info, git_diff, ctx, save_diff_patch_path, diff_info_path
    )


PYGIT_COMMIT_UNSAFE_BEHAVIOUR = os.getenv("PYGIT_COMMIT_UNSAFE_BEHAVIOUR")


def apply_git_revert_patch(ctx: Context, file_path: str) -> None:
    """Apply the saved patch using the cache file for command.

    This command will take the git diff file (most recent file will be selected based on patch provided), clear the diff info and then allow the git diff file patch to be applied, and clear that patch record from the `comment_diff_cache.json` file.
    """

    # Get the repo path
    repo_path = Path(ctx.repo.working_dir)

    # Load diff info file
    diff_info_path, comment_revert_info = load_diff_info(repo_path)

    if not diff_info_path.exists():
        raise ValueError(
            "`comment_diff_cache.json` file does not exist, please use pygit commands first before reverts."
        )

    if comment_revert_info != {}:
        file_path = Path(file_path)

        # Create a save_path variable
        use_diff_patch_path = (
            repo_path / ".pygit_cache/comment" / ctx.git_branch / file_path
        )
        # To remove the .. relative lines
        use_diff_patch_path = use_diff_patch_path.absolute().relative_to(
            repo_path.absolute()
        )
        if (
            len(comment_revert_info[ctx.git_branch][use_diff_patch_path.as_posix()])
            != 0
        ):
            git_diff_file_path = comment_revert_info[ctx.git_branch][
                use_diff_patch_path.as_posix()
            ].pop()

            try:
                diff_process = subprocess.run(
                    ["git", "apply", git_diff_file_path, "--allow-empty"]
                )

                if diff_process.returncode == 0:
                    save_diff_info_file(diff_info_path, comment_revert_info)
                    os.remove(git_diff_file_path)

            except subprocess.CalledProcessError:
                raise CommandFailure(
                    "pygit comment revert failed to run the process, try again or check the files and report the bug to the developers."
                )
        else:
            click.echo("No information stored for reverts on this file.")


def delete_git_saved_patches(ctx: Context) -> None:
    """Delete all the patches generated when the changes are commited by `pygit commit`.

    The function will only be rendered if env variable PYGIT_UNSAFE_BEHAVIOUR = False or not set by the user.
    The function removes the cache files generated by the `pygit comment` and other commands in the CLI package after a particular commit for one particular feature branch.
    """
    # Current branch for deleting info
    curr_branch = ctx.git_branch

    # Repo path
    repo_path = Path(ctx.repo.working_dir)

    # Import the diff info file
    diff_info_path, comment_revert_info = load_diff_info(repo_path)

    # Removing the files related to the current branch and the keys in the comment_diff_cache.json file
    if diff_info_path.exists() and curr_branch in comment_revert_info:
        
        del comment_revert_info[curr_branch]
        shutil.rmtree(diff_info_path.parent / curr_branch)

        save_diff_info_file(diff_info_path, comment_revert_info)
