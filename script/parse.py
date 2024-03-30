import json
import re

def parse_line_to_json(input_file, output_json):
    # Updated pattern to match lines with additional strings before the pattern
    pattern = r".*Time taken for sample (\d+): (\[.*?\]), average: (\d+\.\d+)"
    data = []

    with open(input_file, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                # Extracting values
                sample_id = int(match.group(1))
                # Directly parsing the string that looks like a list into a Python list
                sample_result = json.loads(match.group(2).replace('\'', '\"'))
                average_time = float(match.group(3))
                # Appending to data list
                data.append({
                    "sample_id": sample_id,
                    "sample_result": sample_result,
                    "average_time": average_time
                })

    # Writing to a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
input_file = './workflow.log'
output_json = 'output1.json'
parse_line_to_json(input_file, output_json)

print(f"Data has been successfully written to {output_json}.")

