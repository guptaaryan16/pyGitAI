import subprocess
from subprocess import check_output
from pygitai.context import Context
from typing import Any
from pygitai.exceptions import CommandFailure


def _exclude_from_diff(file):
    return f":(exclude){file}"


def get_staged_diff(ctx: Context, exclude_files=None) -> str:
    """To generate the git diff log output."""

    diff_cached = [
        "git",
        "diff",
        "--cached",
        "--diff-algorithm=minimal",
        f"{ctx.last_commit}"
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
            return None

        diff_process = subprocess.run(
            diff_command, check=True, text=True, stdout=subprocess.PIPE
        )
        diff_output = diff_process.stdout

        return {"files": files_output.split("\n"), "diff": diff_output}

    except subprocess.CalledProcessError as e:
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
        print(f"Error executing git command: {e}")
        return None
