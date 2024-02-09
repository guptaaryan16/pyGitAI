`pygit comment`
-----------------

The command allows you to add docstrings and comments to your code. This command parses your function signature ::


    usage: pygit comment [OPTIONS]

    Add docstrings to a function by providing its name and path using LLM

.. code::
    
    Options:
    --module TEXT                   Specify the module containing the function
    --path TEXT                     Specify the path of the function with
                                    respect to root directory
    --function-name TEXT            Specify the function you want to create
                                    docstrings for
    --docstring-format [Numpy|Google]
    --revert BOOLEAN                Revert the function docstrings generated
      (**experimental**)            earlier due to some errors.
    
    -h                              Generate documentation for the command
    --help                          Show this message and exit.

**General Usage:**

The command is used as follows:

.. code:: bash

    >> pygit comment --path /<repo>/file_name.py --function-name=<function-name>


Sample Input::
    
    def quad(num: int)-> int:
        return num * num * num * num


Sample Output::

    def quad(num: int)-> int:
        """Returns the fourth power of the given integer number.
        
        :param num: The integer number to be squared four times.
        :type num: int
        :raises TypeError: if input is not an integer
        :returns: The fourth power of the given integer number.
        :rtype: int

        :Examples:
            >>> quad(2)
            16
            >>> quad(-3)
            81
        """
        return num * num * num * num



.. note::
    The API is experimental and is subject to change in future depending upon the reception. Please report any issues on the github repo.