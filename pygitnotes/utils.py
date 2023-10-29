import re
import click 
import pygitnotes 


def _extract_messages_from_file(file_path, empty_lines=1)-> list[str]:
    pattern = r"\ncommit: (\d+) Date: (\d{4}-\d{2}-\d{2})\nmessage:\n(.*)\nAuthor: (.*) <(.*)>\n\nPyNote version: \d\n"
    match = re.search(pattern, file_content, re.DOTALL)

    if match:
        # Extract the matched groups
        commit_hash = match.group(1)
        commit_date = match.group(2)
        commit_message = match.group(3)
        commit_author = match.group(4)
        commit_email = match.group(5)

        # Reconstruct the formatted string
    
        print(extracted_string)
    else:
        print("Pattern not found in the file.")
