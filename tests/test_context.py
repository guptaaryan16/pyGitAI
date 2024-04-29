from git import Repo
from pygitai.context import Context
from git import Repo
import pytest
import subprocess
from unittest.mock import patch
import os


@pytest.fixture
def mock_git_diff():
    # Set up a mock Git diff for testing
    return "Mocked Git diff content"


@pytest.fixture
def mock_api_key():
    # Set up a mock API key for testing
    return "mocked_api_key"


def test_context()-> dict:    
    context_sample = {
        'repo': "", 
        'last_commit': "7589c3f8c73da80c54c9a654643e69bd54ebc9fa", 'git_branch': 'main', 
        'ref_branch': 'main', 
        'author': 'Aryan Gupta', 
        'email': 'guptaaryan16@gmail.com', 
        'model_source': 'HF', 
        'model_prop': {
            'auth_token': 'SAMPLE_AUTH_TOKEN', 
            'model': 'Mixtral-8x7B-Instruct-v0.1'
        }, 
        'include_body': False, 
        'body_length': 150, 'git_stack': []
    }

    
    return context_sample
