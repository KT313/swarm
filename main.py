import openai
import subprocess
import os
import json
import time

max_swarm_size = 10
verbose = 3
use_user_input = True


def get_api_key():
    return open("KEY.txt", "r").read().strip()

history = []

def say():
    global history
    global verbose

    if use_user_input:
        input_text = input("Enter text: ")
    else:
        input_text = "Say this is a test!"

    input_text = input_text.replace('"', '\\"')

    history.append({"role": "user", "content": input_text})
    history_json = json.dumps(history)

    api_key = get_api_key()

    def make_curl_command():
        if verbose >= 1:
            curl_command = f"""
            curl https://api.openai.com/v1/chat/completions \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer {api_key}" \
              -d '{{
                 "model": "gpt-3.5-turbo",
                 "messages": {history_json},
                 "temperature": 0.7
               }}'
            """
        else:
            curl_command = f"""
            curl -s https://api.openai.com/v1/chat/completions \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer {api_key}" \
              -d '{{
                 "model": "gpt-3.5-turbo",
                 "messages": {history_json},
                 "temperature": 0.7
               }}'
            """
        return curl_command

    if verbose >= 3:
        print(make_curl_command())
    process = subprocess.run(make_curl_command(), shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    if verbose >= 3:
        print(process.stdout)
    output = json.loads(process.stdout)
    role = output['choices'][0]['message']['role']
    content = output['choices'][0]['message']['content']

    history.append({"role": role.replace('"', '\\"'), "content": content.replace('"', '\\"')})

    return role, content




# main program
current_time = time.time()
history_file_json = f"history/{current_time}.json"
history_file_txt = f"history/{current_time}.txt"


while True:
    try:
        role, content = say()
    except Exception as e:
        print(f"Error: {e}")
        continue

    print(f"Role: {role}")
    print(f"Content: {content}")

    open(history_file_json, "w").write(json.dumps(history))
    with open(history_file_txt, "w") as file:
        for entry in history:
            content = entry['content'].replace('\\"', '"')  # Replace escaped quotes
            line = f"{entry['role']}: {content}"
            file.write(line + "\n")

    if verbose >= 3:
        print(f"History: \n{history}")
