import json
import random

topInterests = json.loads(open("topinterests.json", "r").read())
topPairs = json.loads(open("toppairs.json", "r").read())

finalDict = {"nodes":[], "links":[]}

interestToIndex = {}

index = 0
for couple in topInterests:
	finalDict["nodes"].append({"name": couple[0], "size": couple[1], \
		"group": int(random.random() * 20)})
	interestToIndex[couple[0]] = index
	index += 1

for couple in topPairs:
	pairWords = couple[0]
	words = pairWords.split(',')
	first = words[0]
	second = words[1]
	finalDict["links"].append({"source": interestToIndex[first], \
		"target": interestToIndex[second], "value": couple[1]})

writer = open("nodesandlinks.json", "w")
writer.write(json.dumps(finalDict, sort_keys=True, indent=4))
