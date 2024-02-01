import subprocess
from subprocess import check_output
from pygitai.context import Context
from typing import Any
from pygitai.exceptions import CommandFailure
import os


def _exclude_from_diff(file):
    return f":(exclude){file}"


def get_staged_diff(ctx: Context, exclude_files=None) -> str:
    """To generate the git diff log output."""

    diff_cached = [
        "git",
        "diff",
        "--cached",
        "--diff-algorithm=minimal",
        f"{ctx.last_commit}",
    ]

    files_to_exclude = []
    if exclude_files:
        files_to_exclude = list(map(_exclude_from_diff, exclude_files))

    files_command = diff_cached + ["--name-only"] + files_to_exclude
    diff_command = diff_cached + files_to_exclude

    try:
        files_process = subprocess.run(
            files_command, check=True, text=True, stdout=subprocess.PIPE
        )
        files_output = files_process.stdout.strip()

        if not files_output:
            # If no file is changed, then it should have a similar behaviour as git
            return subprocess.run(
                ["git", "status"], check=True, text=True, stdout=subprocess.PIPE
            ).stdout.strip()

        diff_process = subprocess.run(
            diff_command, check=True, text=True, stdout=subprocess.PIPE
        )
        diff_output = diff_process.stdout

        return diff_output

    except subprocess.CalledProcessError:
        raise CommandFailure(
            "The pygit commit failed to get output for git-staged diff. Try again or raise an issue."
        )


def get_branch_diff(ctx: Context, exclude_files=None):
    """To show the difference between two branches"""
    diff_command = [
        "git",
        "diff",
        ctx.git_branch,
        ctx.ref_branch,
        "--diff-algorithm=minimal",
    ]

    files_to_exclude = []
    if exclude_files:
        files_to_exclude = list(map(_exclude_from_diff, exclude_files))
        diff_command += files_to_exclude

    try:
        diff_process = subprocess.run(
            diff_command, check=True, text=True, stdout=subprocess.PIPE
        )
        diff_output = diff_process.stdout

        return diff_output

    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Error executing git command: {e}")


def get_git_revert_diff_content(
    source_code: str, function_code: str, diff_patch: str, file_path: str
):
    """Git diff generated to allow reverts and thus better code generation from LLMs and a safety check."""
    # Clean the diff patch for output
    # Git diff patch generation
    function_code = "\n".join(function_code.split("\n"))[:-1]

    patch_store_path = f"{file_path}.patch"
    changed_content = source_code.replace(function_code, diff_patch)

    # Now we create a patch file and use that to create a subproces change within git and use that patch
    try:
        with open(patch_store_path, "w") as patch_file:
            patch_file.write(changed_content)

        git_diff_command = f"git diff --no-index {patch_store_path} {file_path}"

        diff_output = subprocess.run(
            git_diff_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        with open(file_path, "w") as original_file:
            original_file.write(changed_content)

        os.remove(patch_store_path)
        
        return diff_output.stdout

    except ValueError:
        raise ValueError(
            "Failed to produce correct patch response for the Function Docstring. Try Again."
        )
