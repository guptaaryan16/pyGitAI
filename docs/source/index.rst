.. pyGitAI documentation master file, created by
   sphinx-quickstart on Sun Dec 31 11:55:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyGitAI
========

Extending `git` with AI!

A python CLI package that contains abstractions over git to make it a bit more smart than it already is, using AI!
 
This app follows traditional Python design philosophy, i.e. to keep it simple and user-friendly.


Introduction 
-------------

The CLI aims to create a plug-and-play ecosystem for all AI models available in the market, even your local trained LLM models, which for instance you can train your model on all your github PRs and files and allow it to generate content as required by your projects. This allows much more flexibility and privacy than expected from LLM APIs and also allows you to harness the power of AI to increase productivity of the developers.

This use of user-chosen models help in generating the boilerplate stuff pretty easily like creating PR content and even generating docstrings and comments for functions ( just support Python for now, more support in future ). 

Also, the long term goal is to integrate this tool with ghstack, Graphite, and other git based CLI tools. Also I want to increase the ease-of-use of AI models in the developer ecosystem space.

Thanks for using this tool. This is my first Python package so please support the project if possible, and forgive me for any poor design choices.

.. note::
   The project is not ready for commercial and enterprise use yet, but we are tyinh to speed the development and add new features as soon as possible. Please consider supporting or contributing to the project on GitHub.

.. image:: ./_static/pygitai_explained.png

Supported LLM Platforms and Models 
-----------------------------------

+-------------------------+-----------------------+-----------+--------------------+
|      LLM Platform       |      Models           | Supported | Commands Supported |
+=========================+=======================+===========+====================+
|                         | - LLAMA-7B            |    ✅     |       ✅           |
|    HuggingFace🤗        |                       +-----------+--------------------+
|    (Inference API)      | - Mixtral-7B Instruct |    ✅     |       ✅           |
+-------------------------+-----------------------+-----------+--------------------+
|                         | - Gemini-Pro          |    ✅     |       ✅           |
|     Google Gemini       |                       +-----------+--------------------+
|                         | - Bard API            |Not Tested | Not Tested         |
|                         |                       +-----------+--------------------+
|                         | - PaLM                |Not Tested | Not Tested         |
+-------------------------+-----------------------+-----------+--------------------+
|                         | - GPT-3.5 Turbo       |Not Tested |    Not Tested      |
|     OpenAI GPT APIs     |                       +-----------+--------------------+
|                         | - GPT-4               | Not Tested| Not Tested         |
+-------------------------+-----------------------+-----------+--------------------+
|                         | - Transformers        |     -     |        -           |
|   Local Model support   |                       +-----------+--------------------+
|                         | - Native PyTorch      |     -     |        -           |
+-------------------------+-----------------------+-----------+--------------------+


.. toctree::
   :maxdepth: 1
   
   installation
   quick-start
   commands
   devnotes
   contributing
   pygitai



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
