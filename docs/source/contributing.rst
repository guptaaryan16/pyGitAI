Contributing Guide 
===================


PyGitAI's Contributing Guide 
-----------------------------

Thank you for considering contributing to PyGitAI! We welcome contributions from the community to help improve and enhance the tool. Please take a moment to review this document for guidelines on how to contribute.

**Prerequisites**

Before you begin contributing, ensure you have the following prerequisites installed:

- Python (version 3.8 and higher)
- Virtualenv (for creating isolated Python environments) or Conda 

**Installation**

1. Clone the repository:

.. code::

    git clone https://github.com/guptaaryan16/pygitai.git

2. Navigate to the project directory:

.. code::

    cd pyGitAI

3. Create and activate a virtual environment:

.. tab::  Using venv (recommended)

    .. code::
        
        virtualenv venv
        source venv/bin/activate   # On Windows: .\venv\Scripts\activate


.. tab:: Using conda vitual environment

    .. code:: 

        conda create -n environment.yaml


4. Install dependencies:

.. code:: 
    
    pip install -r requirements.txt

.. note:: 
    It is not always a good practice to install the practice directly especially something experimental like ``pygitai``.

5. Now you're ready to start contributing!

How to Contribute
-----------------

**Reporting Bugs**

If you encounter a bug, please open an issue on the issue tracker with a detailed description of the problem and steps to reproduce it.

**Suggesting Enhancements**

If you have an idea for an enhancement, open an issue on the issue tracker and provide a clear description of your proposed feature.

**Code Contributions**

1. Fork the repository.
2. Create a new branch:

.. code::

    git checkout -b feature-branch

3. Make your changes and ensure the code follows the coding standards.
4. Write tests for your changes.
5. Ensure all tests pass:

.. code::

    pytest

5. Commit your changes with clear and concise commit messages.
6. Push your changes to your fork:

.. code::

    git push origin feature-branch

7. Submit a pull request to the main repository.


**Documentation**

Improvements to the documentation are always welcome. If you see an opportunity to enhance the documentation, please submit a pull request with your changes.

Development Guidelines
----------------------

**Coding Standards**

Follow PEP 8 and RUFF for Python code style. Ensure your code is readable and well-documented.

**Testing**

Write unit tests for new features and ensure that all existing tests pass before submitting a pull request. ( Under active development )

**Commit Messages**

Write clear and descriptive commit messages. Follow the Conventional Commits specification for consistent and meaningful commit messages. You can always try to use the project and the free APIs to generate the text messages.

**Pull Request Process**

1. Ensure your pull request addresses a specific issue or contributes a valuable enhancement.
2. Provide a clear description of your changes in the pull request.
3. Ensure all tests pass.
4. Request a review from maintainers.
5. Address any feedback received during the review.
6. Once approved, your pull request will be merged.

**Community**

Join our community chat discussions to connect with other contributors and maintainers. We welcome discussions on improvements, bug reports, and general feedback.

**Code of Conduct**

Please read and adhere to our Code of Conduct to ensure a positive and inclusive community.

**License**

By contributing to pyGitAI, you agree that your contributions will be licensed under the LICENSE file associated with the project.

Thank you for contributing to pyGitAI! 🚀