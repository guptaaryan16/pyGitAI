`pygit commit`
-----------------

The command allows you to commit your changes like normal `git commit`. The key change is now you can use an option `--generate-message` or `-gm` that allows you to generate commit messages and commit bodies using LLMs, with option from HF inference APIs, Google Vertex APIs and OpenAI GPT APIs::


    usage: pygit commit [OPTIONS]

    Custom Git Commit Messages to work with LLM models.

.. code::
    
    Options:
    -m, --message TEXT              the commit message for manual commit
    -gm, --generate-message         to generate commit message by LLM model
    -fc, --from-commit TEXT         Last commit hash from which summary is
                                    generated
    --repo-path PATH                path to git repo
    --include-body                  Generate a body along with the commit
    -bl, --body-length INTEGER      Length of body text that needs to be
                                    generated
    -e, --editable                  Edit the commit message in editor before it
                                    is commited
    --editor [vim|nano]             Choose editor: vim or nano
    --commit_type [normal|conventional]
                                    Choose between normal and conventional
                                    styles of commit types
    -h, --help                      show the `pygit commit` help page

Usage:
The command is used as follows:
.. code:: bash

    >> pygit commit --generate-message/-gm # After staging your changes for commit

