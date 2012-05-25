import json, operator

profs = json.loads(open('profiles.json','r').read())

# fixing: motorcycles -> motorcycling, ski -> skiing, travel -> traveling, travelling -> traveling
for i in range(len(profs)):
	interests = profs[i]['interests']
	if interests != []:
		for j in range(len(interests)):
			temp = interests[j].lower().strip()
			if temp == 'motorcycles':
				profs[i]['interests'][j] = 'motorcycling'
			if temp == 'ski':
				profs[i]['interests'][j] = 'skiing'
			if temp == 'travel':
				profs[i]['interests'][j] = 'traveling'
			if temp == 'travelling':
				profs[i]['interests'][j] = 'traveling'

# # getting all the skills and number of occurrences
# allSkills = {}
# for prof in profs:
# 	skills = prof['skills']
# 	if skills != []:
# 		for skill in skills:
# 			skill = skill.lower().strip()
# 			try:
# 				allSkills[skill] += 1
# 			except KeyError:
# 				allSkills[skill] = 1
# with open('allSkills.json', 'a') as f:
# 	f.write(json.dumps(allSkills))
# 
# # getting all interests and number of occurrences
allInterests = {}
for prof in profs:
	interests = prof['interests']
	if interests != []:
		for interest in interests:
			interest = interest.lower().strip()
			# if interest already exists, increment count
			try:
				allInterests[interest] += 1
			# otherwise, add it
			except KeyError:
				allInterests[interest] = 1
# save
with open('allInterests.json','a') as f:
	f.write(json.dumps(allInterests))

# getting all languages and number of occurrences
allLanguages = {}
for prof in profs:
	languages = prof['languages']
	if languages != []:
		for language in languages:
			language = language.lower().strip()
			try:
				allLanguages[language] += 1
			except KeyError:
				allLanguages[language] = 1
sortedLangs = sorted(allLanguages.iteritems(), key = operator.itemgetter(1))

allInts = json.loads(open('allInterests.json','r').read())
allSkills = json.loads(open('allSkills.json','r').read())

# getting the most occurred interests
topInts = {}
for interest in allInts:
	if allInts[interest] > 2:
		topInts[interest] = allInts[interest]
len(topInts)
sortedInts = sorted(topInts.iteritems(), key = operator.itemgetter(1))

# least occurred interests
bottomInts = {}
for interest in allInts:
	if allInts[interest] == 1:
		bottomInts[interest] = allInts[interest]

# num of interests for each popularity (to create a graph, possibly a power law)
numPop = {}
for interest in allInts:
	try:
		numPop[allInts[interest]] += 1
	except KeyError:
		numPop[allInts[interest]] = 1
sortedNumPop = sorted(numPop.iteritems(), key = operator.itemgetter(0))
# sortedNumPop = [(1, 4587), (2, 329), (3, 109), (4, 73), (5, 43), (6, 33), (7, 23), (8, 18), (9, 18), (10, 9), (11, 8), (12, 8), (13, 9), (14, 6), (15, 7), (16, 4), (17, 3), (18, 2), (19, 4), (20, 3), (21, 1), (22, 2), (23, 1), (24, 4), (25, 1), (26, 2), (27, 1), (28, 2), (29, 2), (31, 5), (32, 1), (33, 1), (34, 2), (35, 1), (36, 1), (37, 1), (39, 1), (40, 1), (42, 1), (43, 1), (44, 1), (45, 1), (47, 2), (48, 1), (51, 1), (52, 2), (53, 2), (56, 2), (59, 1), (60, 1), (72, 1), (73, 1), (95, 1), (96, 1), (98, 1), (115, 1), (121, 1), (122, 1), (129, 1), (135, 1), (140, 1), (161, 1), (309, 1)]

# getting co-occuring interests, paired as "biking,hiking": 3
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
len(pairedInts)
with open('pairedInts.json','a') as f:
	f.write(json.dumps(pairedInts))
#sortedPairedInts = sorted(pairedInts.iteritems(), key = operator.itemgetter(1))

import math
# getting Pearson correlations of the links, paired as "biking,hiking": .5
Np = float(len(topInts))
pearsonR = {}
for pair in pairedInts:
	pairS = pair.split(",")
	Na = float(topInts[pairS[0]])
	Nb = float(topInts[pairS[1]])
	Nab = float(pairedInts[pair])
	pR = (Nab * Np - Na * Nb) / math.pow(((Np - Na) * (Np - Nb) * Na * Nb), 0.5)
	pearsonR[pair] = pR
sortedPearsonR = sorted(pearsonR.iteritems(), key = operator.itemgetter(1))

# finding min, max, average of number of interests per profile
num = []
for prof in profs:
	interests = prof['interests']
	if interests != []:
		num.append(len(interests))
mini = 1000
maxi = 0
for n in num:
	if n < mini:
		mini = n
	if n > maxi:
		maxi = n
# mini = 1, maxi = 75
sum(num) / len(num) = 5 # average
# graphing the distribution of number of interests per profile
numInts = {}
for n in num:
	try:
		numInts[n] += 1
	except KeyError:
		numInts[n] = 1
# numInts = {1: 313, 2: 168, 3: 326, 4: 301, 5: 301, 6: 184, 7: 154, 8: 117, 9: 65, 10: 43, 11: 31, 12: 30, 13: 12, 14: 14, 15: 7, 16: 8, 17: 9, 18: 8, 19: 3, 20: 4, 21: 3, 22: 5, 23: 3, 25: 3, 26: 1, 33: 1, 40: 1, 41: 2, 45: 1, 50: 1, 51: 1, 54: 1, 75: 1}

# getting the most occurred skills
topSkills = {}
for skill in allSkills:
	if allSkills[skill] > 5:
		topSkills[skill] = allSkills[skill]
len(topSkills)
sortedSkills = sorted(topSkills.iteritems(), key = operator.itemgetter(1))

# number of profiles per company
for comp in ml:
	print comp['name'] + ': ' + comp['numIDs']

# number of profiles that have various fields filled out
numInterests = 0
interestProfs = []
numSkills = 0
numPositions = 0
numAge = 0
numEducations = 0
numLanguages = 0
numLocation = 0
for prof in profs:
	if prof['interests'] != []:
		numInterests += 1
		interestProfs.append(prof)
	if prof['skills'] != []:
		numSkills += 1
	if prof['positions'] != []:
		numPositions += 1
	if prof['age'] != None:
		numAge += 1
	if prof['educations'] != []:
		numEducations += 1
	if prof['languages'] != []:
		numLanguages += 1
	if prof['location'] != []:
		numLocation += 1
# numInterests = 2122
# numSkills = 1797
# numPositions = 17187
# numAge = 16
# numEducations = 1
# numLanguages = 326
# numLocation = 19448

# getting all companies that these interest-ing people worked at
compsWithInterests = {}
for prof in interestProfs:
	positions = prof['positions']
	if positions:
		for position in positions:
			try:
				compsWithInterests[position['Company name'].lower().strip()] += 1
			except KeyError:
				compsWithInterests[position['Company name'].lower().strip()] = 1
# print companies that appeared more than once
for comp in compsWithInterests:
	if compsWithInterests[comp] > 1:
		print comp + ": " + str(compsWithInterests[comp])
compsWIsorted = sorted(compsWithInterests.iteritems(), key = operator.itemgetter(1))
for comps in compsWIsorted:
	print comps
# saved as numInterestsperComp.txt

# getting profiles from top compsWIsorted companies
RIMinterests = []
for prof in interestProfs:
	positions = prof['positions']
	if positions:
		for position in positions:
			if position['Company name'].lower().strip() == 'research in motion':
				RIMinterests.append(prof)
for prof in RIMinterests:
	with open('profsRIM.json','a') as f:
		f.write(json.dumps(prof) + ',\n')
# saved as profsRIM.json


# getting distribution of locations
profLocation = {}
for prof in profs:
	loc = prof['location']
	if loc:
		try:
			profLocation[loc] += 1
		except KeyError:
			profLocation[loc] = 1
#len(profLocation) = 627
sortedLoc = sorted(profLocation.iteritems(), key = operator.itemgetter(1))

# getting breakdown of companies
profCompanies = {}
for prof in profs:
	positions = prof['positions']
	if positions:
		for position in positions:
			try:
				profCompanies[position['Company name'].lower().strip()] += 1
			except KeyError:
				profCompanies[position['Company name'].lower().strip()] = 1
sortedComps = sorted(profCompanies.iteritems(), key = operator.itemgetter(1))
# getting number of positions in each profile
numPos = {}
for prof in profs:
	positions = prof['positions']
	if positions:
		try:
			numPos[len(positions)] += 1
		except KeyError:
			numPos[len(positions)] = 1
# numPos = {1: 13963, 2: 1924, 3: 719, 4: 297, 5: 132, 6: 71, 7: 30, 8: 17, 9: 9, 10: 9, 11: 3, 12: 4, 34: 1, 15: 1, 16: 1, 18: 1, 20: 1, 21: 1, 22: 1, 24: 1, 30: 1}