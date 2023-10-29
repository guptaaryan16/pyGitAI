from git import InvalidGitRepositoryError


__all__ = [
    'NotAValidGitRepo',
    'NoGPTResponseError',
    'CommandFailure'
]

class Exception(BaseException):
    '''Base exception for all errors in pyGitNotes'''
    pass

class NoGPTResponseError(Exception):
    '''Error in response from GPT model '''
    pass

class NotAGitRepositoryError(Exception):
    '''Exception for Not a valid git repository'''
    pass

class CommandFailure(Exception):
    '''The pyGit command failed. Please report the issue to the developers;-)'''
    pass