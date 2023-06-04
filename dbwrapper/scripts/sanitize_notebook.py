import sys
import json

def readJson(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def stripOutputs(json_data):
    for cell in json_data['cells']:
        cell['outputs'] = []
    return json_data

def writeToFile(file_path, json_data):
    with open(file_path, 'w') as file:
        json.dump(json_data, file)

if len(sys.argv) <= 1:
    print('Usage: python sanitize_notebook.py <filename>.ipynb')
    sys.exit(1)

filename = sys.argv[1]
json_data = readJson(filename)
json_data = stripOutputs(json_data)
writeToFile(filename, json_data)

print(f"sanitized {filename}")
