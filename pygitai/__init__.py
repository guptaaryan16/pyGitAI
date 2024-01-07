import sys


# the change taken from https://www.github.com/ezyang/ghstack
if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata


__version__ = importlib_metadata.version("pygitai")