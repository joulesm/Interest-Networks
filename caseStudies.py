import json, operator

## Research in Motion

profs = json.loads(open('profsRIM.json','r').read())

# checking for duplicates, possible if profile has multiple positions in the same company
for i in range(1, len(profs)):
	for j in range(i):
		if profs[i] == profs[j]:
			print i
# i = 23, 106, 114

# len(RIM) = 136

ints = {}
for prof in profs:
	interests = prof['interests']
	if interests != []:
		for interest in interests:
			interest = interest.lower().strip()
			try:
				ints[interest] += 1
			except KeyError:
				ints[interest] = 1
# len(ints) = 459

# interests that appear more than once
topInts = {}
for interest in ints:
	if ints[interest] > 1:
		topInts[interest] = ints[interest]
# len(topInts) = 66
sortedInts = sorted(topInts.iteritems(), key = operator.itemgetter(1))

# pairs
pairedInts = {}
for prof in profs:
	interests = prof['interests']
	if interests != []:
		# these are the interests in this profile that we care about, popular interests
		popInts = []
		for interest in interests:
			interest = interest.lower().strip()
			try:
				# check each interest to see if it is a topInterest
				s = topInts[interest]
				popInts.append(interest)
			except KeyError:
				pass
		# getting pairs
		if len(popInts) > 1:
			for j in range(1, len(popInts)):
				for k in range(j):
					# alphabetize and stringify with a comma delimiter
					if popInts[j] != popInts[k]:
						if popInts[j] != '' and popInts[k] != '':
							pair = [popInts[j], popInts[k]]
							pair.sort()
							strPair = pair[0] + "," + pair[1]
							# counting how many times this pair occurs
							try:
								pairedInts[strPair] += 1
							except KeyError:
								pairedInts[strPair] = 1
# len(pairedInts) = 326
sortedPairedInts = sorted(pairedInts.iteritems(), key = operator.itemgetter(1))

# number of positions per profile
numPos = {}
for prof in profs:
	positions = prof['positions']
	try:
		numPos[len(positions)] += 1
	except KeyError:
		numPos[len(positions)] = 1
# numPos = {1: 120, 2: 13, 3: 3}

# finding other companies these people worked for
comps = {}
afterComps = []
prevComps = []
for prof in profs:
	positions = prof['positions']
	if len(positions) == 2:
		if positions[0]['Company name'].lower() == "research in motion" and positions[0]['End date'] == None:
			prevComps.append(positions[1]['Company name'])
		elif positions[1]['Company name'].lower() == "research in motion":
			afterComps.append(positions[0])
		else:
			print prof
for prof in profs:
	positions = prof['positions']
	if len(positions) == 3:
		print positions

# average length of time employee has been at RIM
year = {}
for prof in profs:
	positions = prof['positions']
	start = positions[0]['Start date'][0]
	try:
		year[start] += 1
	except KeyError:
		year[start] = 1
# year = {2005: 1, 2007: 1, 2008: 7, 2009: 17, 2010: 28, 2011: 72, 2012: 10}

## Schneider Electric
profs = json.loads(open('profsSE.json','r').read())

# checking for duplicates, possible if profile has multiple positions in the same company
# i = 53, 59, 61
# len(profs) = 62
# len(ints) = 271
# len(topInts) = 28
# len(pairedInts) = 59
# numPos = {1: 57, 2: 3, 3: 1, 4: 1}
# year = {1997: 1, 2005: 3, 2007: 3, 2008: 1, 2009: 8, 2010: 22, 2011: 23, 2012: 1}

## Intel
profs = json.loads(open('profsIntel.json','r').read())

# checking for duplicates, possible if profile has multiple positions in the same company
# i = 5, 8, 23, 32, 48, 53, 55, 62
# len(profs) = 56
# len(ints) = 229
# len(topInts) = 25
# len(pairedInts) = 55
# numPos = {1: 42, 2: 13, 5: 1}
# year = {2005: 2, 2006: 1, 2007: 1, 2008: 2, 2009: 4, 2010: 13, 2011: 26, 2012: 7}

# finding the employees that are interested in energy
profs = json.loads(open('profiles.json','r').read())
for prof in profs:
	interests = prof['interests']
	if interests != []:
		for interest in interests:
			interest = interest.lower().strip()
			if interest == 'efficient homes':
				print prof