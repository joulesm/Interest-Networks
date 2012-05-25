import linkedin2
import helper as h

#################

KEY = 'k1tofeoqr4id'
SECRET = 'KgEvtAPuvFCj1FoE'
RETURN_URL = 'http://localhost'

api = linkedin2.LinkedIn(KEY, SECRET, RETURN_URL)

# token must be True
if not api.request_token():
	print api.get_error()
	sys.exit()

# get oauth_verifier
print 'Go to this URL:'
print api.get_authorize_url()
oauth_verifier = raw_input('Please enter verifier: ')

if not api.access_token(verifier = oauth_verifier):
	print api.get_error()
	sys.exit()

##################

# my user id
#id = api.get_profile(fields = ['id']).id

# my interests, output is one string of all interests
#interests = api.get_profile(member_id = id, fields = ['id', 'interests']).interests
#print 'interests:'
#print interests

# my skills. XML tree of skills - change to list
#skills = api.get_profile(member_id = id, fields = ['id','skills']).skills
#print 'skills:'
#print skills

# get my profile
#julia = api.get_profile()

#connections = api.get_connections(fields = ['id'])
#for connection in connections:
#	print connection.id

# getting as many profile IDs as possible from the predetermined list of companies
#h.getProfilesFromCompanies()

#
IDList = readFile('IDs.txt')
IDskills = []
IDinterests = []
for IDnum in IDList:
	profile = api.get_profile(member_id = IDnum, fields = ['id', 'interests', 'skills'])
	skills = profile.skills
	if len(skills) > 0:
		print skills
		IDskills.append(IDnum)
	interests = profile.interests
	if interests != None:
		print interests
		IDinterests.append(IDnum)

allSkills = []
for IDnum in IDskills:
	profile = api.get_profile(member_id = IDnum, fields = ['id', 'skills'])
	skills = profile.skills
	for skill in skills:
		skill = skill.lower()
		if skill not in allSkills:
			allSkills.append(skill)
allSkills.sort()
saveFile(allSkills, "allSkills.txt")

allInterests = []
for IDnum in IDinterests:
	profile = api.get_profile(member_id = IDnum, fields = ['id', 'interests'])
	interests = profile.interests.split(',')
	for interest in interests:
		interest = interest.strip().lower()
		if interest not in allInterests:
			allInterests.append(interest)
allInterests.sort()
saveFile(allInterests, "allInterests.txt")