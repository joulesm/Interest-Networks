import json
import random
import math

topInterests = json.loads(open("topinterests.json", "r").read())

interestsList = []

for couple in topInterests:
	interestsList.append(couple[0])

writer = open("interestslist.json", "w")
writer.write(json.dumps(interestsList, sort_keys=True, indent=4))