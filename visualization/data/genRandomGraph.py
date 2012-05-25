import json
import random

interests_json_data = open("onlyInterests.json").read()
interestsList = json.loads(interests_json_data)

interestsJson = {"nodes" : [], "links" : []}

# generate all the nodes
for interest in interestsList:
	interestsJson["nodes"].append({"name": interest, "group": int(random.random() * 20)})


#generate the links
numLinks = 100
numInterests = len(interestsJson["nodes"])

for i in range(numInterests):
	randNum = int(random.random() * numInterests)
	while i == randNum:
		randNum = int(random.random() * numInterests)

	interestsJson["links"].append({"value": int(random.random() * 10), "source": i, "target": randNum})




writer = open("interests.json", "w")
writer.write(json.dumps(interestsJson, sort_keys=True, indent=4))
