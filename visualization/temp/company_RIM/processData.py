import json
import random
import math

topInterests = json.loads(open("topinterests.json", "r").read())
topPairs = json.loads(open("toppairs.json", "r").read())
allPairs = json.loads(open("formattedPairs.json").read())
categories = json.loads(open("categories.json").read())
categoriesToIndex = {"GAME": 1, "ART": 3, "MUSIC": 4, "LEARNING": 5, \
					"MOVIES": 6, "BUSINESS": 7, "FOOD": 8, "TRAVEL": 9, "TECHNOLOGY": 11, \
					"LANGUAGE": 13, "PEOPLE": 14, "FINANCE": 15, \
					"HEALTH": 16, "FUN": 17 }

finalDict = {"nodes":[], "links":[]}

interestToIndex = {}
interestToValue = {}
allInterestsInAllPairs = {}

index = 0
Np = 0

def findInterestSize(interest):
	for couple in topInterests:
		if interest == couple[0]:
			frequency = couple[1]
			interestToValue[interest] = frequency
			return max(min(frequency/2, 30), 5)
	return 0

def getCategory(interest):
	for category in categories:
		for i in categories[category]:
			if interest == i:
				return categoriesToIndex[category]

	print interest
	return 0
	

for pair in allPairs:
	both = pair.split(',')
	first = both[0]
	second = both[1]

	if first not in allInterestsInAllPairs:
		allInterestsInAllPairs[first] = 1

	if second not in allInterestsInAllPairs:
		allInterestsInAllPairs[second] = 1


for couple in topPairs:
	words = couple[0].split(',')
	if words[0] not in interestToIndex:
		finalDict["nodes"].append({"name": words[0], \
			"group": getCategory(words[0]), "size": findInterestSize(words[0])})
		interestToIndex[words[0]] = index
		index += 1

	if words[1] not in interestToIndex:
		finalDict["nodes"].append({"name": words[1], \
			"group": getCategory(words[1]), "size": findInterestSize(words[1])})
		interestToIndex[words[1]] = index
		index += 1


Np = len(allInterestsInAllPairs)

for couple in topPairs:
	pairWords = couple[0]
	words = pairWords.split(',')
	first = words[0]
	second = words[1]
	Na = interestToValue[first]
	Nb = interestToValue[second]
	Nab = couple[1]
	corrConst = (Nab * Np - Na * Nb) / math.sqrt((Np - Na) * (Np - Nb) * Na * Nb)
	if corrConst >= 0:
		finalDict["links"].append({"source": first, \
			"target": second, "value": corrConst})

#clear all link-less interests
interestsWithLinks = []
for link in finalDict["links"]:
	interestsWithLinks.append(interestToIndex[link["source"]])
	interestsWithLinks.append(interestToIndex[link["target"]])


interestToRemove = []
for i in range(len(finalDict["nodes"])):
	if i not in interestsWithLinks:
		interestToRemove.append(finalDict["nodes"][i]["name"])

for interest in interestToRemove:
	for i in range(len(finalDict["nodes"])):
		if finalDict["nodes"][i]["name"] == interest:
			finalDict["nodes"].pop(i)
			break

#fix links
interestToIndex = {}
for i in range(len(finalDict["nodes"])):
	interestToIndex[finalDict["nodes"][i]["name"]] = i

for link in finalDict["links"]:
	a = link["source"] 
	b = link["target"]
	link["source"] = interestToIndex[a]
	link["target"] = interestToIndex[b]

#generate interestslist
interestslist = []
for i in finalDict["nodes"]:
	interestslist.append(i["name"])


writer = open("nodesandlinks.json", "w")
writer2 = open("interestslist.json", "w")
writer.write(json.dumps(finalDict, sort_keys=True, indent=4))
writer2.write(json.dumps(interestslist, sort_keys=True, indent=4))
