from configparser import ConfigParser
from git import Repo


class Context:
    """Context to understand the git-repo and API calls to the Model and Github.

    The :py:class:`pygitai.Context` object controls the information exchange between the CLI environment and the LLM model. All the subsequent features will also be dependent on `Context` and attributes must be added here only for increasing the information to LLM models.

    Attributes:
        * repo (:py: classgit.Repo): The git repo currently in use (default = './')
        * last_commit: The reference commit for the `git diff`
        * git_branch: Current git branch in use.
        * ref_branch: Reference branch for the project(default='main')
        * author: Author in git config file.
        * email: Email in git config file.
        * model_source : The model source currently in use (OpenAI or HF)
        * model_prop(dict): The model properties for currently available    
    """

    def __init__(self, config: ConfigParser, repo: Repo):
        """
        To initailize the context for generating commit titles and messages
        """

        # git Repo Details
        self.repo = repo

        try:
            self.last_commit = repo.head.commit
        except ValueError:
            self.last_commit = None  # Current bug for repo with no commit

        self.git_branch = repo.head.reference.name

        # config for message details
        self.ref_branch = config.get("git", "ref-branch")
        self.author = config.get("git", "author")
        self.email = config.get("git", "email")

        # model properties
        self.model_source = config.get("default", "default_platform")
        self.model_prop = dict(config[self.model_source])

        # optional attributes
        self.include_body = False
        self.body_length = 150

        # Git command stack
        self.git_stack = []