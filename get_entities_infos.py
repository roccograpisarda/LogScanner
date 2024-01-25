import re
import os
import json
import csv

def extract_entities_until_stop(log_file_path):
    # Initialize a list to store entity data
    all_entities = []

    # Open and read the log file
    with open(log_file_path, 'r') as file:
        log_entries = file.read()

    # Use regular expressions to find and extract entities
    entity_pattern = r'"entities": \[(.*?)\]'
    matches = re.findall(entity_pattern, log_entries, re.DOTALL)

    found_stop = False  # Flag to indicate if we found the stop string

    # Initialize a set to store unique entity name and value combinations
    unique_combinations = set()

    # Iterate through the matches and extract the entity data
    for match in matches:
        entity_data = re.findall(r'"name": "(.*?)",\s+"value": "(.*?)"', match)

        for entity_name, entity_value in entity_data:
            # Check if the stop string is found in this match
            if "   1)" in match:
                found_stop = True
                break

            # Exclude entities with "sys." prefix and check if the entity value is not empty
            if not entity_name.startswith("sys.") and entity_value.strip():
                unique_combinations.add((entity_name, entity_value))

    # Return the extracted entity data as a list of tuples and the flag indicating if the stop string was found
    return list(unique_combinations), found_stop

def get_entity_names_in_entities_folder():
    entity_names = []
    entities_folder = "entities"
    for filename in os.listdir(entities_folder):
        if filename.endswith("_entries_en.json"):
            entity_name = filename.replace("_entries_en.json", "")
            entity_names.append(entity_name)
    return entity_names

def load_entity_values(entity_name, language="en"):
    values = []
    entries_path = os.path.join("entities", f"{entity_name}_entries_{language}.json")
    if os.path.exists(entries_path):
        with open(entries_path, 'r') as file:
            entries = json.load(file)
            for entry in entries:
                value = entry["value"]
                synonyms = entry.get("synonyms", [])
                values.append((value, synonyms))
    return values

def calculate_value_coverage(entity_values, entity_data):
    total_values = len(entity_values)
    matched_values = 0

    for value, synonyms in entity_values:
        if entity_data == value or entity_data in synonyms:
            matched_values += 1

    return (matched_values / total_values) * 100 if total_values > 0 else 0

# Define a function to save the results in a CSV file
def save_results_as_csv(results, output_file_path):
    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Entity Name", "Entity Value", "Value Coverage"])
        for entity_name, entity_value, value_coverage in results:
            writer.writerow([entity_name, entity_value, f"{value_coverage:.2f}%"])

def main():
    # Define the path to your log file
    log_file_path = "output_log.txt"

        # Check if the "entities" folder exists
    entities_folder = "entities"
    if not os.path.exists(entities_folder):
        print("No entities found.")
        return

    # Call the function to extract entities until encountering "   1)"
    extracted_entities, found_stop = extract_entities_until_stop(log_file_path)

    # Create the necessary directories
    os.makedirs(os.path.join("results", "entities"), exist_ok=True)

    # Save the results to a file in the "entities" subfolder of the "results" folder
    output_file_path = os.path.join("results", "entities", "entity_coverage_results.csv")

    coverage_results = []

    # Get the entity names from the "entities" folder
    entity_names_in_folder = get_entity_names_in_entities_folder()

    # Iterate through the extracted entities
    for entity_name, entity_value in extracted_entities:
        # Exclude entities with "sys." prefix and check if the entity value is not empty
        if not entity_name.startswith("sys.") and entity_name in entity_names_in_folder and entity_value.strip():
            # Load possible values from the associated JSON files
            entity_values = load_entity_values(entity_name)

            # Calculate value coverage considering synonyms
            value_coverage = calculate_value_coverage(entity_values, entity_value)

            coverage_results.append((entity_name, entity_value, value_coverage))

    save_results_as_csv(coverage_results, output_file_path)

    # Print all the extracted entity data
    for entity_name, entity_value, value_coverage in coverage_results:
        print(f"Entity Name: {entity_name}, Entity Value: {entity_value}, Value Coverage: {value_coverage:.2f}%")

    if found_stop:
        print("Found '   1)', stopped processing.")

if __name__ == "__main__":
    main()
