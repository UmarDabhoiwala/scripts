#!/usr/bin/env python3
import subprocess
import sys
from openai import OpenAI
import os

def ask_gpt_for_commit_message(text) -> str:
    api_key = os.getenv('OPENAI_API_KEY')

    if api_key is None:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key = api_key)

    practices = """
    The commit message should adhere to the best practice 50/72 rule.

    Separate subject from body with a blank line
    Limit the subject line to 50 characters
    Capitalise the subject line
    Do not end the subject line with a period
    Use the imperitive mood in the subject line
    Wrap the body at 72 characters
    Use the body to explain what and why vs how
    """

    format = """

    short_title for the commit

    DS-XXXX (number for the branch)

    - Dot Points explaining changes
    -
    -
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant designed to write commit messages based on git differences follow these practices {practices}"},
            {
                "role": "user",
                "content": f"Write a commit message for this git diff {text}, return it in this format {format}",
            }
        ],
    )

    return response.choices[0].message.content


def commit_changes(diff_file):
    # Attempt to read the diff file to ensure it exists and has content
    try:
        with open(diff_file) as file:
            diff_content = file.read()
    except FileNotFoundError:
        print(f"The file {diff_file} was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Check if there are any changes to commit
    if not diff_content.strip():
        print("No changes to commit.")
        return

    changes = diff_content.strip()

    try:
        commit_message = ask_gpt_for_commit_message(changes)
    except Exception as e:
        print(f"Failed to generate commit: {e}")


    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to commit changes: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python commit_changes.py <diff_output_file>")
        sys.exit(1)

    diff_file = sys.argv[1]
    commit_changes(diff_file)




