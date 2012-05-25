import json
import operator

allInts = json.loads(open('allInterests.json','r').read())

topInts = {}
for interest in allInts:
	if allInts[interest] > 2:
		topInts[interest] = allInts[interest]

len(topInts)
sortedInts = sorted(topInts.iteritems(), key = operator.itemgetter(1), reverse = True)

writer = open('topinterests.json', 'w')

writer.write(json.dumps(sortedInts, sort_keys=True, indent=4))