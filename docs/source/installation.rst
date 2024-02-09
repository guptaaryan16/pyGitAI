Installation
============

Welcome to the installation guide for `pygitai`.

Prerequisites
-------------

Before you begin the installation, make sure you have the following prerequisites installed:

- Python (version 3.8 and higher)
- pip (Python package installer)

Using pip
----------

Use the command for installing PyGitAI::
   
   pip install -U pygitai


Install From Source
--------------------

There is a way to install the package from source and its recommended for contributing to the package. For more information, refer contributing guide as well.

You can install pyGitAI using the following steps:

1. **Create a Virtual Environment (Optional):**

   It's recommended to create a virtual environment to isolate the project dependencies. Run the following commands in your terminal::
 
      python -m venv pygitai_dev
      source pygitai_dev/bin/activate  # Activate the virtual environment (use "activate" on Windows)
   
2. **Git Clone the repository**
   
   Now lets clone the github repository and then use it to install the application from source ::

      git clone https://github.com/guptaaryan16/pyGitAI.git
      cd pyGitAI

3. **Install using pip** 
   
   Now install the package using an editable option using pip::
      
      pip intall -e .