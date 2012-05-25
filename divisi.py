from csc import divisi2

matrix = divisi2.network.conceptnet_matrix('en')

# run SVD
U, S, V = matrix.normalize_all().svd(k = 100)

# get similar concepts
sim = divisi2.reconstruct_similarity(U, S, post_normalize = False)
sim.row_named('teach').top_items(10)
sim.entry_named('horse', 'cow')

# related concepts, spreading activation
assoc = divisi2.network.conceptnet_assoc('en')
U, S, _ = assoc.svd(k = 100)
spread = divisi2.reconstruct_activation(U, S)

spread.entry_named('cat', 'dog')
spread.row_named('think').top_items()

# separating out interests that don't exist in Divisi
allInts = json.loads(open('allInterests.json','r').read())
topInts = {}
for interest in allInts:
	if allInts[interest] > 2:
		topInts[interest] = allInts[interest]
# fix has words that need adjusting to find in Divisi
fix = []
found = []
for interest in topInts:
	try:
		s = spread.row_named(interest).top_items(10)
		found.append(interest)
	except KeyError:
		fix.append(interest)
len(found) # 129
len(fix) # 320

# fixing words that aren't found in Divisi
fixed = []
notfixed = []
for tofix in fix:
	print tofix
	keep = raw_input('new word?')
	if keep == '?':
		notfixed.append(tofix)
	else:
		fixed.append(keep)

# measuring similarity between all the interests
similar = []
for i in range(1, len(found)):
	for j in range(i):
		s = sim.entry_named(found[i], found[j])
		similar.append([found[i], found[j], s])
similar.sort(key = operator.itemgetter(2))

# measuring relatedness between all the interests
related = []
for i in range(1, len(found)):
	for j in range(i):
		s = spread.entry_named(found[i], found[j])
		related.append([found[i], found[j], s])
related.sort(key = operator.itemgetter(2))
# similarity seems to be a better measure

# making categories of the paired interests with threshold of .4
categories = []
for s in similar:
	if s[2] > .2:
		# check to see if category exists
		exists = False
		for cat in categories:
			try:
				cat.index(s[0])
				try:
					cat.index(s[1])
					exists = True
					# both interests are in the category
				except ValueError:
					cat.append(s[1])
					exists = True
					# 0 existed, 1 didn't, adding 1 to category
			except ValueError:
				try:
					cat.index(s[1])
					cat.append(s[0])
					exists = True
					# 0 didn't exist, 1 did, adding 0 t category
				except ValueError:
					pass
					# do nothing until entire categories is checked
		if exists == False:
			categories.append([s[0], s[1]])
# categories
[u'literature', u'art', u'sport', u'news', u'basketball', u'dance', u'science', u'soccer', u'entertainment', u'football', u'baseball', u'ski', u'music', u'design', u'jazz', u'education']
[u'guitar', u'acoustic guitar', u'music', u'classical music', u'poetry', u'piano', u'entertainment', u'jazz', u'education', u'art', u'dance']
[u'sport', u'tennis', u'art', u'basketball', u'dance', u'science', u'soccer', u'entertainment', u'football', u'baseball', u'ski', u'music', u'design', u'jazz', u'education']
[u'cinema', u'theatre', u'television', u'theater', u'movies']
[u'education', u'research', u'entertainment']
[u'design', u'dance', u'sport', u'soccer', u'entertainment', u'football', u'baseball', u'ski', u'music', u'art', u'jazz', u'education']
[u'wine', u'apple']
[u'church', u'theater', u'cinema', u'television', u'movies', u'faith', u'theatre', u'religion']
[u'business', u'job']
[u'faith', u'religion', u'church']
[u'food', u'coffee']
[u'travel', u'traveling']

sport = [u'sport', u'basketball', u'soccer', u'entertainment', u'football', u'baseball', u'ski']
art = [u'guitar', u'acoustic guitar', u'music', u'classical music', u'poetry', u'piano', u'jazz',  u'art', u'dance', u'design']
learning = [u'education', u'research', u'literature', u'news', u'science']
movies = [u'theater', u'cinema', u'television', u'movies', u'theatre']
work = [u'business', u'job']
religion = [u'faith', u'religion', u'church']
food = [u'food', u'coffee', u'wine', u'apple']
travel = [u'travel', u'traveling']

# curated, we start with these categories
sportCat = divisi2.category(u'sport', u'basketball', u'soccer', u'entertainment', u'football', u'baseball', u'ski')
artCat = divisi2.category(u'guitar', u'acoustic guitar', u'music', u'classical music', u'poetry', u'piano', u'jazz',  u'art', u'dance', u'design')
learningCat = divisi2.category(u'education', u'research', u'literature', u'news', u'science')
moviesCat = divisi2.category(u'theater', u'cinema', u'television', u'movies', u'theatre')
workCat = divisi2.category(u'business', u'job')
religionCat = divisi2.category(u'faith', u'religion', u'church')
foodCat = divisi2.category(u'food', u'coffee', u'wine', u'apple')
travelCat = divisi2.category(u'travel', u'traveling')

sport_features = divisi2.aligned_matrix_multiply(sport, matrix)
sport_features.to_dense().top_items()
sim.left_category(sport).top_items()
sim.left_category(sport).entry_named('run')

catList = [sport, art, learning, movies, work, religion, food, travel]
catMatrix = [sportCat, artCat, learningCat, moviesCat, workCat, religionCat, foodCat, travelCat]
catString = ['sport', 'art', 'learning', 'movies', 'work', 'religion', 'food', 'travel']

# removing interests we've already categorized
needCat = []
usedCat = []
for cat in catList:
	for i in range(len(cat)):
		usedCat.append(cat[i])
for interest in found:
	try:
		s = usedCat.index(interest)
	except ValueError:
		needCat.append(interest)

# calculating the categories for other interests
catzInterests = []
for interest in needCat:
	temp = [interest]
	for i in range(len(catMatrix)):
		temp.append([catString[i], sim.left_category(catMatrix[i]).entry_named(interest)])
	catzInterests.append(temp)
len(catzInterests)

# returns the highest related category for this interest
def maxCategory(catz):
	maxC = catz[1]
	for i in range(2, len(catz)):
		if catz[i][1] > maxC[1]:
			maxC = catz[i]
	return maxC

for ints in catzInterests:
	maxC = maxCategory(ints)
	if maxC[1] > .2:
		print ints[0] + ": " + maxC[0] + " " + str(maxC[1])
		catList[catString.index(maxC[0])].append(ints[0])

# updated categories using a maxC[1] > .2:
sport = [u'sport', u'basketball', u'soccer', u'entertainment', u'football', u'baseball', u'ski', u'table tennis', u'tennis', u'chess', u'golf', u'hockey', u'badminton', u'ice hockey']
art = [u'guitar', u'acoustic guitar', u'music', u'classical music', u'poetry', u'piano', u'jazz', u'art', u'dance', u'design', u'salsa', u'photograph', u'science fiction', u'fashion', u'painting', u'photography', u'culture', u'nature', u'creativity', u'audio']
learning = [u'education', u'research', u'literature', u'news', u'science', u'history', u'communication', u'mathematics']
movies = [u'theater', u'cinema', u'television', u'movies', u'theatre', u'gym', u'film']
work = [u'business', u'job']
religion = [u'faith', u'religion', u'church']
food = [u'food', u'coffee', u'wine', u'apple', u'family']
travel = [u'travel', u'traveling']

# new categories
sportCat = divisi2.category(u'sport', u'basketball', u'soccer', u'entertainment', u'football', u'baseball', u'ski', u'table tennis', u'tennis', u'chess', u'golf', u'hockey', u'badminton', u'ice hockey')
artCat = divisi2.category(u'guitar', u'acoustic guitar', u'music', u'classical music', u'poetry', u'piano', u'jazz', u'art', u'dance', u'design', u'salsa', u'photograph', u'science fiction', u'fashion', u'painting', u'photography', u'culture', u'nature', u'creativity', u'audio')
learningCat = divisi2.category(u'education', u'research', u'literature', u'news', u'science', u'history', u'communication', u'mathematics')
moviesCat = divisi2.category(u'theater', u'cinema', u'television', u'movies', u'theatre', u'gym', u'film')
workCat = divisi2.category(u'business', u'job')
religionCat = divisi2.category(u'faith', u'religion', u'church')
foodCat = divisi2.category(u'food', u'coffee', u'wine', u'apple', u'family')
travelCat = divisi2.category(u'travel', u'traveling')

# fixing words that aren't found in Divisi
notfixed = []
for tofix in fix:
	print tofix
	keep = raw_input('new word?')
	if keep == '?':
		notfixed.append(tofix)
	else:
		try:
			s = sim.row_named(keep)
			needCat.append(keep)
		except KeyError:
			notfixed.append(tofix)
# removing duplicates
notfixed = list(set(notfixed))
needCat = list(set(needCat))
len(notfixed) = 147
len(needCat) = 200

# notfixed = [u'strategic planning', u'ps3', u'startups', u'change management', u'crossfit', u'motorsport', u'board games', u'road biking', u'supply chain management', u'water skiing', u'...', u'web services', u'industrial design', u'college football', u'usability research', u'itil', u'new ventures', u'social networking', u'voip', u'real estate investing', u'corporate financial reporting', u'kitesurfing', u'online marketing', u'crm', u'public relations', u'renewable energy', u'ted', u'web 3.0', u'game design', u'process improvement', u'seo', u'product development', u'sustainable design', u'sociology', u'internet marketing', u'new gadgets', u'outsourcing', u'telecommunications', u'social networks', u'new technology', u'fine dining', u'hci', u'emerging technologies', u'formula 1', u'social media', u'web technologies', u'professional networking', u'mma', u'home automation', u'toplinked', u'data visualization', u'racquetball', u'etc', u'weight lifting', u'retail', u'electronic music', u'human rights', u'consulting', u'public speaking', u'water sports', u'graphic design', u'linux', u'ecommerce', u'personal development', u'pr', u'interface design', u'open source', u'business process improvement', u'sustainable development', u'jet skiing', u'working out', u'interior design', u'crowdsourcing', u'knowledge management', u'rock climbing', u'emerging technology', u'operating systems', u'international business', u'web design', u'lion500', u'wireless', u'management training', u'mountain climbing', u'contemporary art', u'alpine skiing', u'horse riding', u'spending time with friends and family', u'scrapbooking', u'genealogy', u'video games', u'machine learning', u'mobile gaming', u'product design', u'new business development', u'business management', u'graphic arts', u'product management', u'etc.', u'scuba', u'cad', u'f1', u'leadership training', u'reference requests', u'management consulting', u'online games', u'it', u'linkedin', u'social entrepreneurship', u'gadgets', u'business intelligence', u'cognitive science', u'pervasive computing', u'cuisine', u'triathlon', u'computer graphics', u'user experience', u'software architecture', u'music production', u'hr', u'kickboxing', u'digital', u'triathlons', u'android', u'martial arts', u'web development', u'long distance running', u'six sigma', u'technology management', u'new media', u'sustainability', u'paintball', u'pilates', u'wakeboarding', u'lacrosse', u'emerging markets', u'aikido', u'and spending time with my family.', u'spending time with family and friends', u'international development', u'skying', u'computer games', u'cloud computing', u'business strategy', u'snowmobiling', u'information visualization', u'interaction design', u'embedded systems']

# remove items already categorized
stillneedCat = []
usedCat = []
for cat in catList:
	for i in range(len(cat)):
		usedCat.append(cat[i])
for interest in needCat:
	try:
		s = usedCat.index(interest)
	except ValueError:
		stillneedCat.append(interest)
needCat = stillneedCat

# calculate categories for these interests
# find ones greater than .2

game = [u'basketball', u'soccer', u'entertainment', u'football', u'baseball', u'table tennis', u'tennis', u'chess', u'golf', u'hockey', u'badminton', u'ice hockey', u'volleyball', u'poker', u'cricket', u'rugby', u'box', u'team', u'squash', u'softball', u'billiards']
sport = [u'sport', u'ski', u'hike', u'canoe', u'snowboard', u'bike', u'skateboard', u'climb', u'jog', u'hunt', u'bicycle', u'hunt', u'skydive', u'outdoors', u'outdoor', u'gym', u'cycle', u'marathon', u'motorcycle', u'kayak', u'automobile', u'yoga', u'row', u'karate', u'windsurf', u'backpack', u'judo', u'equestrian', u'fitness', u'raft', u'rollerblade']
art = [u'poetry', u'art', u'dance', u'design', u'salsa', u'photograph', u'science fiction', u'fashion', u'painting', u'photography', u'culture', u'nature', u'creativity', u'drawing', u'inspiration', u'knit', u'sew', u'touch', u'woodworking', u'fine art', u'arts', u'architecture', u'comic']
music = [u'guitar', u'acoustic guitar', u'music', u'classical music', u'piano', u'jazz', u'audio', u'opera']
learning = [u'education', u'research', u'literature', u'news', u'science', u'history', u'communication', u'mathematics', u'philosophy', u'psychology', u'biology', u'astronomy', u'economics', u'politics', u'environment', u'statistic']
movies = [u'theater', u'cinema', u'television', u'movies', u'theatre', u'film', u'video', u'animation']
work = [u'business', u'job', u'career', u'trade', u'carpentry', u'real estate', u'management', u'entrepreneur', u'operation', u'journalism', u'media', u'efficient', u'analysis', u'invite', u'strategy', u'lion', u'health']
religion = [u'faith', u'religion', u'church']
food = [u'food', u'coffee', u'wine', u'apple', u'bake', u'cook', u'dine', u'brew', u'cigar']
travel = [u'travel', u'traveling', u'fly', u'aviation', u'trek']
technology = [u'web', u'internet', u'technology', u'database', u'online', u'nanotechnology', u'artificial intelligence', u'robot', u'blog', u'ruby', u'electronics', u'electronic', u'prototype', u'innovation', u'compute', u'signal', u'network', u'broadcast', u'mobile', u'engineer', u'security', u'vision', u'use', u'blackberry']
places = [u'africa', u'china', u'india', u'europe', u'middle east']
language = [u'spanish', u'italian', u'japanese']
people = [u'family', u'friends', u'mentor', u'coach', u'people', u'charity', u'community', u'volunteer', u'leadership', u'organize', u'behavior', u'collaboration', u'service']

gameCat = divisi2.category(u'basketball', u'soccer', u'entertainment', u'football', u'baseball', u'table tennis', u'tennis', u'chess', u'golf', u'hockey', u'badminton', u'ice hockey', u'volleyball', u'poker', u'cricket', u'rugby', u'box', u'team', u'squash', u'softball', u'billiards')
sportCat = divisi2.category(u'sport', u'ski', u'hike', u'canoe', u'snowboard', u'bike', u'skateboard', u'climb', u'jog', u'hunt', u'bicycle', u'hunt', u'skydive', u'outdoors', u'outdoor', u'gym', u'cycle', u'marathon', u'motorcycle', u'kayak', u'automobile', u'yoga', u'row', u'karate', u'windsurf', u'backpack', u'judo', u'equestrian', u'fitness', u'raft', u'rollerblade')
artCat = divisi2.category(u'poetry', u'art', u'dance', u'design', u'salsa', u'photograph', u'science fiction', u'fashion', u'painting', u'photography', u'culture', u'nature', u'creativity', u'drawing', u'inspiration', u'knit', u'sew', u'touch', u'woodworking', u'fine art', u'arts', u'architecture', u'comic')
musicCat = divisi2.category(u'guitar', u'acoustic guitar', u'music', u'classical music', u'piano', u'jazz', u'audio', u'opera')
learningCat = divisi2.category(u'education', u'research', u'literature', u'news', u'science', u'history', u'communication', u'mathematics', u'philosophy', u'psychology', u'biology', u'astronomy', u'economics', u'politics', u'environment', u'statistic')
moviesCat = divisi2.category(u'theater', u'cinema', u'television', u'movies', u'theatre', u'film', u'video', u'animation')
workCat = divisi2.category(u'business', u'job', u'career', u'trade', u'carpentry', u'real estate', u'management', u'entrepreneur', u'operation', u'journalism', u'media', u'efficient', u'analysis', u'invite', u'strategy', u'lion', u'health')
religionCat = divisi2.category(u'faith', u'religion', u'church')
foodCat = divisi2.category(u'food', u'coffee', u'wine', u'apple', u'bake', u'cook', u'dine', u'brew', u'cigar')
travelCat = divisi2.category(u'travel', u'traveling', u'fly', u'aviation', u'trek')
technologyCat = divisi2.category(u'web', u'internet', u'technology', u'database', u'online', u'nanotechnology', u'artificial intelligence', u'robot', u'blog', u'ruby', u'electronics', u'electronic', u'prototype', u'innovation', u'compute', u'signal', u'network', u'broadcast', u'mobile', u'engineer', u'security', u'vision', u'use', u'blackberry')
financeCat = divisi2.category(u'finance', u'commerce', u'invest', u'investment', u'ad', u'advertise', u'brand')
placesCat = divisi2.category(u'africa', u'china', u'india', u'europe', u'middle east')
languageCat = divisi2.category(u'spanish', u'italian', u'japanese')
peopleCat = divisi2.category(u'family', u'friends', u'mentor', u'coach', u'people', u'charity', u'community', u'volunteer', u'leadership', u'organize', u'behavior', u'collaboration', u'service')

catList = [game, sport, art, music, learning, movies, work, religion, food, travel, technology, finance, places, language, people]
catMatrix = [gameCat, sportCat, artCat, musicCat, learningCat, moviesCat, workCat, religionCat, foodCat, travelCat, technologyCat, financeCat, placesCat, languageCat, peopleCat]
catString = ['game', 'sport', 'art', 'music', 'learning', 'movies', 'work', 'religion', 'food', 'travel', 'technology', 'finance', 'places', 'language', 'people']

# do similarity and spread activation on leftover interests
similar = []
for i in range(1, len(needCat)):
	for j in range(i):
		s = sim.entry_named(needCat[i], needCat[j])
		similar.append([needCat[i], needCat[j], s])
similar.sort(key = operator.itemgetter(2))
related = []
for i in range(1, len(needCat)):
	for j in range(i):
		s = spread.entry_named(needCat[i], needCat[j])
		related.append([needCat[i], needCat[j], s])
related.sort(key = operator.itemgetter(2))