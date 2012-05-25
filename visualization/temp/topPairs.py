import json
import operator

allPairs = json.loads(open('pairedInts.json','r').read())

topPairs = {}
for pair in allPairs:
	if allPairs[pair] > 1:
		topPairs[pair] = allPairs[pair]

print len(topPairs)
sortedPairs = sorted(topPairs.iteritems(), key = operator.itemgetter(1), reverse = True)

writer = open('toppairs.json', 'w')

writer.write(json.dumps(sortedPairs, sort_keys=True, indent=4))