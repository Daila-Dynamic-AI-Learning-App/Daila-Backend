"""
    prompter module
"""
import openai
from engine import redis_client
import re
import keys
import json

openai.api_key = keys.OPEN_API_KEY

def getPrompt(user_input: str, end: bool) -> str:
    """
        Takes in user and/or assistant respnses to
        be used in the openai module

        Args:
            user_input: User's question
            assistant_response: assistant's response
    """
    if end:
       user_message = {'role': 'user', 'content': 'give links to the resources'}
    else:
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
        model="gpt-3.5-turbo",
        messages=data
    )

    assistant_response = response['choices'][0]['message']['content']
    stripped = assistant_response.strip('\n').strip()
    pattern = r'.*\d:\s(.*\?)'
    result = re.findall(pattern, stripped)

    if len(result) > 0:
        assistant = { 'role': 'assistant', 'content': stripped }
        redis_client.addToList('chat_log', assistant)
        return result[0]
    return stripped
