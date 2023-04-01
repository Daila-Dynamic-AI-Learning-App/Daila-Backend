"""
    prompter module
"""
import openai
from engine import redis_client
import re
import keys
import json
from typing import Tuple
from engine import redis_client

openai.api_key = keys.OPEN_API_KEY

def getPrompt(user_input: str, first: bool) -> Tuple[str, bool]:
    """
        Takes in user response and gives thw assistant's 
        response

        Args:
            user_input: User's question
            first: wants the first question/prompt
    """
    assesment = False

    # check if first and clear all content of the list to be used
    if first:
        redis_client.delete('chat_log')

    user_message = {'role': 'user', 'content': user_input}
    redis_client.addToList('chat_log', user_message)

    # decode bytes list in UTF-8
    chat_log = redis_client.allList('chat_log')
    str_list = [ byt.decode('utf8') for byt in chat_log ]

    # join contents of string list with comma
    json_string = '[' + ','.join(str_list) + ']'
    # load the string as a json object
    data = json.loads(json_string)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=data
    )

    assistant_response = response['choices'][0]['message']['content']
    stripped = assistant_response.strip('\n').strip()
    
    # regex to extract the questions in the assistant response
    pattern = r'.*\d:\s(.*\?)'
    result = re.findall(pattern, stripped)

    assistant = { 'role': 'assistant', 'content': stripped }
    redis_client.addToList('chat_log', assistant)

    # check if the assessment is done
    if stripped.startswith('End$'):
        assesment = True
        # remove the identifier from the stripped response
        return (stripped[len('End$'):], assesment)

    if len(result) > 0:
        return (result[0], assesment)
    return (stripped, assesment)
