import json

reader = open('allinterests.txt', 'r')
writer = open('interests.json', 'w')

preListOfInterests = reader.readlines()
postListOfInterests = []

for interest in preListOfInterests:
	postInterest = interest.replace("\n", "")
	postListOfInterests.append(postInterest)

writer.write(json.dumps(postListOfInterests))

