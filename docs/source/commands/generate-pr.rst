`pygit generate-pr`
--------------------

The command allows you to commit your changes like normal `git generate-pr`. The key change is now you can use an option `--generate-message` or `-gm` that allows you to generate PR title and content using LLMs, with option from HF inference APIs, Google Vertex APIs and OpenAI GPT APIs::


    Usage: pygit generate-pr [OPTIONS]

    Generate PR changes along with title and body for merge with repos
    (for small issues) on the feature branch

.. code::
    
    Options:

    --body-length INTEGER         PR body length
    --ref-branch TEXT             default reference branch to generate commit
    --from-commit TEXT            the commit from which the PR message should be
                                    generated
    -i_n, --issue-number INTEGER  default reference branch to generate commit
    --authors LIST                list PR author names to add in the message
    --pr-type [|conventional]     list PR author names to add in the message
    -h, --help                    show the `pygit generate` help page


**Usage:**

The command is used as follows:

.. code:: bash

    >> pygit generate-pr -gm/--generate-message # After commiting changes on the feature branch


.. note::
    The command cannot be used for changes on the main branch but only for feature branches. The idea is to use the git diff generated 
    from these feature branches to create the PR titles and body messages and thus help the developers automate more tasks. 
