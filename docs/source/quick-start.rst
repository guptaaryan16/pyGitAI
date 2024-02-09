Quick-Setup
============

Welcome to the setup guide for PyGitAI CLI app.
You can setup `PyGitAI` with the following steps:

1. **Obtain LLM model API keys**

.. tab:: Google API (Recommended)

    Here is a nice tutorial for requesting Google Gemini API keys. You can request for the same before 
    setting up the pygit project. 
    https://ai.google.dev/tutorials/setup


.. tab:: HuggingFace APIs

    Refer the docs for HuggingFace Inference APIs for the models you want to generate the API keys for.
    https://huggingface.co/docs/api-inference/index
        

.. tab:: OpenAI chat APIs
      
    You can refer to OpenAI docs for getting API keys. This way is less recommended as the APIs are paid and have similar
    performance on most tasks. You can see the OpenAI docs here: https://platform.openai.com

2. **Run pygit setup command**

   It's recommended to create a virtual environment to isolate the project dependencies. Run the following commands in your terminal:

   .. code:: bash
         
         >> cd your-project-directory
         >> pygit setup
         
   Now follow the step-by-step instruction process, this allows you to setup up the pygit config files that will be helpful using the commands.

   Now you are ready to use the pygit commands. Yay!

3. **Extra step (Read About commands and Using them correctly)**

You can refer to the :doc:`commands <./commands>`  for more details about the usage of the CLI tool.
