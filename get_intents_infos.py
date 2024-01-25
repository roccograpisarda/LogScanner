import os
import re
import json
from datetime import datetime, timedelta
# Initialize a variable to store the previous timestamp
previous_timestamp = None

def extract_convo_value(log_data, chatbot_name):
    global previous_timestamp
    pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z)\sbotium-core-Convo\s([^{\n]+)'

    match = re.search(pattern, log_data)
    if match:
        timestamp = match.group(1)
        
        # Convert the timestamps to datetime objects for comparison
        current_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Check if the timestamp is different from the previous entry and within a 1-second tolerance
        if previous_timestamp is None or (current_time - previous_timestamp) >= timedelta(seconds=0.241):
            #print(timestamp)
            previous_timestamp = current_time
            value = match.group(2)
            # Extract only the text before the first forward slash ("/")
            value_parts = value.split("/")
            #print(value_parts)

            if value_parts:
                if len(value_parts) > 2:
                    if(chatbot_name == "roomreservation-chatbot"):
                        extracted_value = value_parts[0].split("_")[0].split(" -")[0]
                    else: 
                        if(chatbot_name != "ecoomerce-aaql"):
                            extracted_value = value_parts[2].split("_")[0].split(".")[0].replace("-"," ")
                            print(extracted_value)
                        else: 
                            extracted_value = value_parts[2].split("_")[0].split(".")[0]
           
                    #print(extracted_value)
                else:
                    extracted_value = value_parts[0].split("-")[0]
                # Check if the extracted value contains "BotiumError:" and return None
                if "BotiumError:" in extracted_value:
                    return None
                else:
                    return extracted_value

    return None




def extract_intent_name_from_line(log_data):
    pattern = r'"name":\s*"([^"]+)"'

    match = re.search(pattern, log_data)
    if match:
        return match.group(1)
    else:
        return None

def extract_intent_values_from_file(file_path):
    results = []
    next_line_is_intent = False

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if next_line_is_intent:
                    intent_value = extract_intent_name_from_line(line)
                    if intent_value:
                        results.append(intent_value)
                    next_line_is_intent = False
                elif '    "intent": {' in line:
                    next_line_is_intent = True
    except FileNotFoundError:
        print("File not found. Please provide the correct file path.")

    return results

def extract_convo_values_from_file(file_path, chatbot):
    results = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                convo_value = extract_convo_value(line, chatbot)
                if convo_value:
                    results.append(convo_value)
    except FileNotFoundError:
        print("File not found. Please provide the correct file path.")

    return results


def get_project_name():
    file_path= "botium.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        project_name = data.get("botium", {}).get("Capabilities", {}).get("PROJECTNAME")

        if project_name:
            return project_name
        else:
            return "PROJECTNAME not found in the JSON file."
    except FileNotFoundError:
        return "File not found: " + file_path
    except json.JSONDecodeError:
        return "Error decoding JSON data in the file."


def main():
    # Specify the path to your text file
    file_path = 'output_log.txt'
    chatbot = get_project_name ()

    # Extract conversation values from the log file
    convo_values = extract_convo_values_from_file(file_path, chatbot)
    
    # Extract intent values from the log file
    intent_values = extract_intent_values_from_file(file_path)

    # Create a set for matching values
    matching_values = set()

    # Check for matching values
    for convo_value in convo_values:
        if convo_value in intent_values:
            matching_values.add(convo_value)

    # Create the "results" folder with an "intents" subfolder
    results_folder = 'results'
    intents_folder = os.path.join(results_folder, 'intents')
    os.makedirs(intents_folder, exist_ok=True)

    # Save matching values to "matching_values.txt"
    if matching_values:
        with open(os.path.join(intents_folder, 'matching_values.txt'), 'w') as matching_file:
            for value in matching_values:
                matching_file.write(f"Matching Value: {value}\n")
                print(f"{value}")
        print(f"Number of matching values: {len(matching_values)}")

    # Save conversation values to "convo_values.txt"
    if convo_values:
        with open(os.path.join(intents_folder, 'convo_values.txt'), 'w') as convo_file:
            for convo_value in convo_values:
                convo_file.write(f"Convo Name: {convo_value}\n")

    # Save intent values to "intent_values.txt"
    if intent_values:
        with open(os.path.join(intents_folder, 'intent_values.txt'), 'w') as intent_file:
            for intent_value in intent_values:
                intent_file.write(f"Intent Name: {intent_value}\n")
    else:
        print("No intent values found.")

if __name__ == "__main__":
    main()
