import openai
import subprocess
import os
import json
import time
import re
import pickle

max_swarm_size = 5
verbose = 0
use_user_input = True
confirm_each_agent = False

max_tokens = -1
n = 1
temperature = 0.7

# model = "gpt-3.5-turbo"
model = "gpt-4-1106-preview"





















# ------------------ DO NOT EDIT BELOW THIS LINE ------------------

# check if KEY.txt exists
if not os.path.exists("KEY.txt"):
    print("ERROR: KEY.txt does not exist. Please create KEY.txt and paste your API key in it.")
    exit(1)

# make sure chats folder exists
os.makedirs("chats", exist_ok=True)

# count number of folders in chats folder
chat_folders = os.listdir("chats")
chat_num = len(chat_folders)
selected_chat = -1

if chat_num > 0:
    inp = input(f"Found {chat_num} chats. Continue existing chat? (y/n): ")
    if inp == "y":
        # list all chats
        for i in range(len(chat_folders)):
            print(f"{i}: {chat_folders[i]}")
        inp2 = int(input("Enter chat number: "))
        if inp2 < chat_num:
            selected_chat = inp2
            print("\n\n")
        else:
            print("Invalid input. Starting new chat.")
    else:
        print("Starting new chat.")

if selected_chat == -1:
    inp3 = input("Enter new chat name: ")
    chat_name = inp3
else:
    chat_name = chat_folders[selected_chat]

current_swarm_size = 1
first_step = True
if selected_chat == -1:
    agents = [] # [["agent1", history], ["agent2", history], ...]
else:
    agents = pickle.load(open(f"chats/{chat_name}/agents.pkl", "rb"))


def get_api_key():
    return open("KEY.txt", "r").read().strip()

api_key = get_api_key()
    
def make_curl_command(history_in):
    history_json_in = json.dumps(history_in)

    if verbose >= 3:
        print(f"JSON being sent:\n{history_in}")

    data = {
        "model": model,
        "messages": history_in,
        "temperature": temperature,
        "n": n
    }

    if max_tokens > 0:
        data["max_tokens"] = max_tokens

    curl_command = ["curl"]

    if verbose < 1:
        curl_command.append("-s")

    curl_command.extend([
        "https://api.openai.com/v1/chat/completions",
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {api_key}",
        "-d", json.dumps(data)
    ])

    # print(curl_command)
    return curl_command

if selected_chat == -1:
    history = []
else:
    history = pickle.load(open(f"chats/{chat_name}/history.pkl", "rb"))

# if loading existing chat, show history
if selected_chat != -1:
    for entry in history:
        print(f"----------\n{entry['role']}")
        print(f"{entry['content']}\n")


system_text = f"""
you are an agent designed to handle complex tasks. \
to handle complex tasks, you can split the complex tasks into easier \
sub-tasks and give them to other agents. you can talk to another agent \
with the following command: \
$system_call('agent_name', 'instruction'). \
if an agent with the name agent_name does not yet exist, it will be \
created. you can call multiple agents at once and they will respond to you \
after your message. Create specialized agents to efficiently solve tasks. \
The maximum amount of agents you are allowed to create is {max_swarm_size-1}. Do not create more than {max_swarm_size-1} agents! \
Make sure to use the correct command syntax when calling an agent: "$system_call('agent_name', 'instruction')"! \
Don't forget to call this command after you have decided which agents to use.\
"""

# system_text = system_text.replace('"', '\\"')
if selected_chat == -1:
    history.append({"role": "system", "content": system_text})


def check_system_call(input_string):
    pattern = r"\$system_call\('([^']+)',\s*'([^']+)'\)"
    matches = re.findall(pattern, input_string)
    array = [list(match) for match in matches]
    if verbose >= 3:
        print(array)
    return array



def say():
    global history
    global verbose
    global first_step

    if not use_user_input and first_step and selected_chat == -1:
        input_text = "give a short overview about how linux works. use 2 agents to write the different sections. Keep it very short and also tell your agents to keep it very short."
        first_step = False
    else:
        input_text = input("Enter text: ")


    if input_text != "":
        input_text = input_text.replace('"', '\\"')
        
        if verbose >= 3:
            print("2")
        
        history.append({"role": "user", "content": input_text})
    
    if verbose >= 3:
        print("3")

    try:
        process = subprocess.run(make_curl_command(history), shell=False, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        if verbose >= 3:
            print(process.stdout)
    except Exception as e:
        print(f"----------\nError: \n{e}\n----------")    
    
    if verbose >= 3:
        print("4")

    output = json.loads(process.stdout)
    role = output['choices'][0]['message']['role']
    content = output['choices'][0]['message']['content']

    history.append({"role": role.replace('"', '\\"'), "content": content.replace('"', '\\"')})

    return role, content




# main program
history_file_json = f"chats/{chat_name}/history.json"
history_file_txt = f"chats/{chat_name}/history.txt"


while True:
    if verbose >= 3:
        print("1")
    try:
        role, content = say()
    except Exception as e:
        print(f"Error: {e}")
        break

    print(f"--------------------\n{role}")
    print(f"{content}\n")
    
    # make sure chat folder exists
    os.makedirs(f"chats/{chat_name}", exist_ok=True)

    # save chat
    pickle.dump(history, open(f"chats/{chat_name}/history.pkl", "wb"))
    pickle.dump(agents, open(f"chats/{chat_name}/agents.pkl", "wb"))

    system_calls = check_system_call(content)
    if system_calls is not []:
        for part in system_calls:
            agent_name = part[0]
            content = part[1]
            if confirm_each_agent:
                print(f"calling agent {agent_name} with this content: \n{content}\nCONFIRM with any input:")
                input("")

            # check if agent exists 
            agent_exists = False
            counter = 0
            history_index = -1
            index = 0
            if agents is not []:
                for part in agents:
                    if part[0] == agent_name:
                        agent_exists = True
                        history_index = counter
                        if verbose >= 3:
                            print(f"{agent_name} already exists")
                    else:
                        counter += 1
            
            #prepare history for that agent
            if verbose >= 3:
                print(f"agents array: {agents}")
            if not agent_exists:
                if current_swarm_size >= max_swarm_size:
                    if verbose >= 3:
                        print(f"ERROR: You are only allowed to create {max_swarm_size-1} agents!")
                    history.append({"role": "system", "content": f"ERROR: Could not create {agent_name}. Current agent count: {current_swarm_size}. You are only allowed to create {max_swarm_size-1} agents!"})
                    print(f"----------\nsystem")
                    print(f"ERROR: Could not create {agent_name}. Current agent count: {current_swarm_size}. You are only allowed to create {max_swarm_size-1} agents!\n")
                    continue
                agents.append([agent_name, []])
                current_swarm_size += 1
                if verbose >= 3:
                    print(f"agents array after initializing new agent: {agents}")
                index = len(agents)-1
            else:
                index = history_index
            
            if verbose >= 3:
                print(f"adding to history:\ncontent: {content}")
            agents[index][1].append({"role": "assistant".replace('"', '\\"'), "content": content.replace('"', '\\"')})
            if verbose >= 3:
                print(f"agents array after adding to history: {agents}, index was {index}")
            
            # send message
            try:
                process = subprocess.run(make_curl_command(agents[index][1]), shell=False, check=True, stdout=subprocess.PIPE, universal_newlines=True)
                if verbose >= 3:
                    print(process.stdout)
            except Exception as e:
                print(f"----------\nError: \n{e}\n----------")    
            
            output = json.loads(process.stdout)
            role = output['choices'][0]['message']['role']
            content = output['choices'][0]['message']['content']

            print(f"--------------------\n{agent_name}")
            print(f"{content}\n")
            
            # get reply
            agents[index][1].append({"role": "function".replace('"', '\\"'), "name": agent_name.replace('"', '\\"'), "content": (f"Agent: {agent_name} \n"+content).replace('"', '\\"')})
            history.append({"role": "function".replace('"', '\\"'), "name": agent_name.replace('"', '\\"'), "content": (f"Agent: {agent_name} \n"+content).replace('"', '\\"')})
        
        # save chat
        pickle.dump(history, open(f"chats/{chat_name}/history.pkl", "wb"))
        pickle.dump(agents, open(f"chats/{chat_name}/agents.pkl", "wb"))


    open(history_file_json, "w").write(json.dumps(history))
    with open(history_file_txt, "w") as file:
        for entry in history:
            content = entry['content'].replace('\\"', '"')  # Replace escaped quotes
            line = f"----------\n{entry['role']}: \n----------\n{content}"
            file.write(line + "\n")

    if verbose >= 3:
        print(f"History: \n{history}")
