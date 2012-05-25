import json

json_data = open('pairedInts.json').read()

temp = json.loads(json_data)

writer = open('formattedPairs.json', 'w')

writer.write(json.dumps(temp, sort_keys=True, indent=4))