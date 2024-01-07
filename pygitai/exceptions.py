from git import InvalidGitRepositoryError


class Exception(BaseException):
    """Base exception for all errors in pyGitAI"""

    pass


class NotValidConfig(Exception):
    """Not a Valid config. If config file is present, delete it and then setup config with `pygit setup`."""

    pass


class NoGPTResponseError(Exception):
    """Error in response from GPT model"""

    pass


class NotAGitRepositoryError(InvalidGitRepositoryError):
    """Exception for Not a valid git repository"""

    pass


class CommandFailure(Exception):
    """The pyGit command failed. Please report the issue to the developers;-)"""

    pass


__all__ = [  # noqa: F822
    "NotAValidGitRepo",
    "NoGPTResponseError",
    "CommandFailure",
    "NotValidConfig",
]
