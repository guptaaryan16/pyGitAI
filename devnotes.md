Developer Notes
===============


Setup commands and Environment Options:
---------------------------------------
- `Choose_Model_Type`: Local, OpenAI or HuggingFace models chat completion models 

- `Model_Location_Path / API keys`: Either OpenAI or HuggingFace chat API( More APIs will be supported in the future )

- `Directory`: to store the commit messages and hashes and the changes for the PRs and Commit bodies ( default=./pygit_cache ) ( follows standard Python cache dir requirements )
- `Git Author and Email`: git config author and email


Command line requirements(first supported commands and options):
----------------------------------------------------------------
- A function that can just create the necessary commit with all the required commit messages and the generated body 
` pygit commit -—generate-title -—generate-body `

- A cmd line that can push the commit to the branch and generate the pull request w.r.t branch 
` pygit generate -—PR-title -—PR-body `

-  The command to list the messages generated previously (may add the ability to use these for final PR title and note)
` pygit list —-title -—PR-title `


Workflow (Expected, Again I am new to Python based development :-| )
--------------------------------------------------------------------
We need to create the command line messages by giving the git diff arguments to the ChatGPT and other tools and they have to understand the changes in the files and generate the commit title, commit body and PR title and PR body.

This can be done by fetching the command messages and the `git diff` and then se them to make a query to the OpenAI GPT modeld or a local model downloaded using diffusers library. The library follows a convenient choice in the choice of functions and the environment to make sure devs have flexibility and companies can keep privacy in the codebases, 


New Ideas(May be implemented with no deadline in mind right now :-\)
---------------------------------------------------------------------
1. To-Do app for what to be implemented with the branches
2. Try to shift the codebase towards low level languages like Rust or C++.
3. The API should support making Plugins for the VS code and other git based CLI tools like ghstack and Graphite
4. The documentation can be something like click with less support for an API guide as it is a CLI application.
5. The docs should be rebuilt with great CSS.
6. The long term aim is to make small changes happen directly by the developers and 
have tools like copilot CLI to understand and improve the developer workflows. 