import os
import sys
import gzip
from typing import List
from pydantic import BaseModel, Field

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.schema import OutputParserException



model = "mixtral"

class ScriptInfo(BaseModel):
    """
    Model for LLM output structure
    """
    error: List[str] = Field(description="Erros in the logs.")
    risk: List[str] = Field(description="Risk in the logs.")

parser = PydanticOutputParser(pydantic_object=ScriptInfo)

# Update the prompt to match the new query and desired format.
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(
            "answer the users question as best as possible.\n{format_instructions}\n{question}"
        )
    ],
    input_variables=["question"],
    partial_variables={
        "format_instructions": parser.get_format_instructions(),
    },
)

# chat model for mixtral
chat_model = ChatOllama(
    model="mixtral:latest",
)

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
    _input = prompt.format_prompt(question=query_string)
    output = chat_model(_input.to_messages())
    return output


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

            llm_output = analyse_logs(file_string=content)
            print(llm_output.content)
            print("* * * * *")
            print("")
       

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ollama-log-analysis.py <log_directory_path>")
    else:
        log_directory = sys.argv[1]
        if is_valid_directory(log_directory):
            search_logs_and_analyse(log_directory)
        else:
            print(f"Error: {log_directory} is not a valid directory.")