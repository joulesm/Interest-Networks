import json

json_data = open('interests.json').read()

temp = json.loads(json_data)

writer = open('p-interests.json', 'w')

writer.write(json.dumps(temp, sort_keys=True, indent=4))