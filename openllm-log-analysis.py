## It is in development, some errors may appear.
 
import os
import sys
import gzip
from typing import List



import os, openai, typing as t
from openai.types.chat import (
  ChatCompletionMessageParam,
  ChatCompletionUserMessageParam,
)

client = openai.OpenAI(base_url=os.getenv('OPENLLM_ENDPOINT', 'http://localhost:3000') + '/v1', api_key='na')

models = client.models.list()
print('Models:', models.model_dump_json(indent=2))
model = models.data[0].id

# Chat completion API
stream = str(os.getenv('STREAM', False)).upper() in ['TRUE', '1', 'YES', 'Y', 'ON']


# chat model for mixtral
chat_model = ChatOpenAI(openai_api_base='http://localhost:3000', timeout=300, openai_api_key='na')

def read_log_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def read_gzipped_log_file(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        content = file.read()
    return content

def is_valid_directory(directory_path):
    return os.path.isdir(directory_path)

def analyse_logs(file_string):
    """
    Analyse job script using LLM model
    """
    query_string = (f"please tell about the erros in the logs?\n"
    f"please tell the about the risk detected in the logs?\n"
    f"{file_string}\n"
    )

    messages: t.List[ChatCompletionMessageParam]= [
    ChatCompletionUserMessageParam(role='user', content=query_string),]

    completions = client.chat.completions.create(messages=messages, model=model, max_tokens=128, stream=stream)

    print(f'Chat completion result (stream={stream}):')
    if stream:
        for chunk in completions:
            text = chunk.choices[0].delta.content
            if text:
                print(text, flush=True, end='')
    else:
        print(completions)

    parsed_data = parse_chatcompletion_output(completions)

    if parsed_data:
        unique_lines = set(parsed_data['content'].split('\n'))
        for line in unique_lines:
            print(line)
    else:
        print("Failed to parse response")



def search_logs_and_analyse(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if 'log' in file and '.gz' in file:
                gzipped_log_file_path = os.path.join(root, file)
                content = read_gzipped_log_file(gzipped_log_file_path)
                print(f"Log Summary of {gzipped_log_file_path}:\n")
            elif 'log' in file:
                log_file_path = os.path.join(root, file)
                content = read_log_file(log_file_path)
                print(f"Log Summary of {log_file_path}:\n")

            analyse_logs(file_string=content)
            



class ChatCompletionMessage:
    def __init__(self, content, role, function_call=None, tool_calls=None):
        self.content = content
        self.role = role
        self.function_call = function_call
        self.tool_calls = tool_calls

class Choice:
    def __init__(self, finish_reason, index, logprobs, message):
        self.finish_reason = finish_reason
        self.index = index
        self.logprobs = logprobs
        self.message = message

class ChatCompletion:
    def __init__(self, id, choices, created, model, object, system_fingerprint, usage):
        self.id = id
        self.choices = choices
        self.created = created
        self.model = model
        self.object = object
        self.system_fingerprint = system_fingerprint
        self.usage = usage

class CompletionUsage:
    def __init__(self, completion_tokens, prompt_tokens, total_tokens):
        self.completion_tokens = completion_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens

def parse_chatcompletion_output(response):
    try:
        choices = response.choices
        if choices:
            last_choice = choices[0]
            message = last_choice.message
            return {
                "role": message.role,
                "content": message.content,
            }
        else:
            return None
    except (AttributeError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return None



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ollama-log-analysis.py <log_directory_path>")
    else:
        log_directory = sys.argv[1]
        if is_valid_directory(log_directory):
            search_logs_and_analyse(log_directory)
        else:
            print(f"Error: {log_directory} is not a valid directory.")