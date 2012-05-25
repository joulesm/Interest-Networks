import sys
import json
import string

# reads the file, returns list of lines
# used for reading the list of companies or profile IDs
def readFile(file):
	f = open(file, 'r')
	fileList = []
	for line in f:
		fileList.append(line.rstrip())
	return fileList

# gets profile ID only if field isn't private
def getID(profile):
	profileID = profile.id
	if profileID == 'private':
		return None
	else:
		return profileID

# stores a profileID at the end of the file
def saveID(profileID):
	IDFile = './IDs.txt'
	with open(IDFile, 'a') as f:
		f.write(str(profileID) + '\n')
	return

# stores a profile with relevant fields in a JSON file
def saveProfile(profile):
	#jProfile = JSONifyProfile(profile)
	jProfile = profile
	profileFile = 'profiles.json'
	with open(profileFile, 'a') as f:
		f.write(json.dumps(jProfile) + ',\n')
	return

# reads in list of ML companies, splits list to those we can and can't get financial info for
def getPublicCompanies():
	cIDs = json.loads(open('ML_comp_profiles.txt', 'r').read())
	for cID in cIDs:
		print cID
		keep = raw_input('Use or not? y/n ')
		if keep.lower() == 'y':
			with open('./ML_public_comps.txt', 'a') as f:
				f.write(json.dumps(cID) + ',\n')
		else:
			with open('./ML_other_comps.txt', 'a') as f:
				f.write(json.dumps(cID) + ',\n')
	
	return
	
# stores all the gathered profile IDs from a given list of company IDs
def getPIDsFromCIDs(api, cIDs):
	search_size = 25
	search_cap = 28 # max search results = 700
	for cID in cIDs:
		company = cID['name']
		# getting search results
		profiles = []
		for i in range(search_cap):
			start = search_size * i
			param = 'company-name=' + company + '&start=' + str(start) + '&count=25'
			search = api.profile_search(param)
			if search:
				profiles.append(search)
		# getting/saving profile IDs
		for profileL in profiles:
			for profile in profileL:
				#print profile
				profileID = getID(profile)
				if profileID is not None:
					saveID(profileID)
	return

# counts number of IDs we get per company ID
def countCIDs(api, cID, IDs):
	
	search_size = 25
	search_cap = 28
	
	company = cID['name']
	numCIDs = 0
	profiles = []
	for i in range(search_cap):
		start = search_size * i
		param = 'company-name=' + company + '&start=' + str(start) + '&count=25'
		search = api.profile_search(param)
		if search:
			numCIDs += len(search)
			print numCIDs
			profiles.append(search)
	
	for profileL in profiles:
		for profile in profileL:
			profileID = getID(profile)
			if profileID is None:
				numCIDs -= 1
				print numCIDs
			else:
				try:
					IDs.index(profileID)
				except ValueError:
					numCIDs -= 1
					print numCIDs
	
	return numCIDs

# gets all relevant fields of a profile
def getFields(profID):
	return api.get_profile(member_id = profID, fields = ['id', 'date-of-birth', 'educations', 'skills', 'interests', 'languages', 'location', 'positions'])

# returns age from either date-of-birth or estimated from last education
def getAge(profile):
	bday = None
	if profile.date_of_birth:
		bday = profile.date_of_birth
	elif profile.educations:
		if profile.educations[0].end_date:
			bday = profile.educations[0].end_date - 22
		elif profile.educations[0].start_date:
		 	bday = profile.educations[0].start_date - 18
	
	if bday:
		return 2012 - int(bday)
	else:
		return None
	

# returns education in a nice list
def getEducations(profile):
	e = []
	
	for education in profile.educations:
		school = ''
		field = ''
		degree = ''
		start = None
		end = None
		
		if education.school_name:
			school = education.school_name
		if education.field_of_study:
			field = education.field_of_study
		if education.degree:
			degree = education.degree
		if education.start_date:
			start = education.start_date
		if education.end_date:
			end = education.end_date
		
		e.append({"School": school, "Field of study": field, "Degree": degree, "Start date": start, "End date": end})
	
	return e

def getPositions(profile):
	p = []
	
	for position in profile.positions:
		ID = ''
		name = ''
		title = ''
		summary = ''
		start = None
		end = None
		
		if position.companyID:
			ID = position.companyID
		if position.company:
			name = position.company
		if position.title:
			title = position.title
		if position.summary:
			summary = position.summary
		if position.start_date:
			start = position.start_date
		if position.end_date:
			end = position.end_date
		
		p.append({"Company ID": ID, "Company name": name, "Title": title, "Summary": summary, "Start date": start, "End date": end})
	
	return p

# pulls out relevant fields from the profile and makes a JSON string:
# { }
def JSONifyProfile(profile):
	#profile = getFields(profID)
	ID = profile.id
	skills = []
	interests = []
	languages = []
	location = ''
	educations = []
	positions = []
	age = ''
	
	try:
		ID = profile.id
		if profile.skills:
			skills = profile.skills
		if profile.interests:
			interests = profile.interests.split(',')
		if profile.languages:
			languages = profile.languages
		if profile.location:
			location = profile.location
		if profile.educations:
			educations = getEducations(profile)
		if profile.positions:
			positions = getPositions(profile)
		age = getAge(profile)
	except:
		pass
	
	p = {"id": ID, "age": age, "skills": skills, "interests": interests, "languages": languages, "location": location, "educations": educations, "positions": positions}
	
	return p

def getLocations(company):
	l = []
	
	if company.otherLocations:
		for location in company.otherLocations:
			loc = location.split(',')
			l.append({"city": loc[0], "state": loc[1], "postal": loc[2], "country": loc[3]})
	
	return l

def JSONifyCompany(company):
	ID = company.id
	name = ''
	companyType = ''
	industry = ''
	specialties = []
	ticker = ''
	size = ''
	hq = ''
	locations = []
	
	try:
		ID = company.id
		name = company.universal_name
		companyType = company.company_type
		industry = company.industry
		specialties = company.specialties
		ticker = company.ticker
		size = company.size
		hq = company.hq
		locations = getLocations(company)
	except:
		pass
	
	c = {"id": ID, "name": name, "type": companyType, "industry": industry, "specialties": specialties, "ticker": ticker, "size": size, "hq": hq, "locations": locations}
	
	return c