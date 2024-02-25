#!/usr/bin/env python3
from openai import OpenAI
import sys
import argparse
import os

def main():

    parser = argparse.ArgumentParser(description="Interface with ChatGPT")

    parser.add_argument('message', nargs='*', help='Message to send to ChatGPT')

    parser.add_argument('--convo', action='store_true', help='Example flag that can modify behavior')

    args = parser.parse_args()

    message_string = ' '.join(args.message)

    continous = False

    if args.convo:
        continous = True
        print("Flag is set")


    api_key = os.getenv('OPENAI_API_KEY')

    if api_key is None:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key = api_key)


    ask_gpt_for_commit_message(client,message_string, continous)

def ask_gpt_for_commit_message(client, message, is_continous = False) -> str:

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Respond to the user's queries."}
    ]

    while True:
        # Append user message to the conversation
        messages.append({
            "role": "user",
            "content": message,
        })

        # Make the API call
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )

        # Extract the response text
        response_text = response.choices[0].message.content
        print(response_text)

        # Append system (assistant's) response
        messages.append({"role": "assistant", "content": response_text})

        # exit if not in continous mode
        if not is_continous:
            break


        message = input("You: ")
        if message.lower() == 'quit':
            break

    return response_text

if __name__ == "__main__":

    main()