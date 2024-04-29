#!/bin/bash

# Define logs and error paths
set -xeu

# Setup the git repository
mkdir tests/repo
cd tests/repo
git init 

API_KEY=$0

# Setup pygit config and test files 
pygit setup << EOF
1  # Choice for type of model (replace with your desired value)
$API_KEY 
1  # Model Id 
y  # Is the current branch ref branch for the project? (y or n)
n  # Enter the Ref branch for the project (if the previous answer was 'n')
y  # Is the current author correct? (y or n)
n  # Enter the current author (if the previous answer was 'n')
Github # Username 
github@example.com  # Enter the email
y  # Is the current path the root of the project? (y or n)
EOF

# Now Lets make a command and commit for the file 
mv ../scripts/math.py math.py

