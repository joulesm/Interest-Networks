
__version__ = "1.9"

# Provides a Pure Python LinkedIn API Interface.

try:
	import sha
except DeprecationWarning, derr:
	import hashlib
	sha = hashlib.sha1

import urllib, time, random, httplib, hmac, binascii, cgi, string, datetime
import oauth2 as oauth
import urlparse
from HTMLParser import HTMLParser

from xml.dom import minidom
from xml.sax.saxutils import unescape

class OAuthError(Exception):
	# General OAuth exception, nothing special.
	def __init__(self, value):
		self.parameter = value

	def __str__(self):
		return repr(self.parameter)

class Stripper(HTMLParser):
	# Stripper class that strips HTML entity.
	def __init__(self):
		HTMLParser.__init__(self)
		self.reset()
		self.fed = []

	def handle_data(self, d):
		self.fed.append(d)

	def getAlteredData(self):
		return ''.join(self.fed)

class XMLBuilder(object):
	def __init__(self, rootTagName):
		self.document = minidom.Document()
		self.root = self.document.createElement(rootTagName)
		self.document.appendChild(self.root)

	def xml(self):
		return self.document.toxml()

	def __unicode__(self):
		return self.document.toprettyxml()

	def append_element_to_root(self, element):
		self.root.appendChild(element)

	def append_list_of_elements_to_element(self, element, elements):
		map(lambda x:element.appendChild(x),elements)
		return element

	def create_element(self, tag_name):
		return self.document.createElement(str(tag_name))

	def create_element_with_text_node(self, tag_name, text_node):
		text_node = self.document.createTextNode(str(text_node))
		element = self.document.createElement(str(tag_name))
		element.appendChild(text_node)
		return element

	def create_elements(self, **elements):
		return [self.create_element_with_text_node(tag_name, text_node) for tag_name, text_node in elements.items()]

class Education(object):
	# Class that wraps an education info of a user
	def __init__(self):
		self.id = None
		self.school_name = None
		self.degree = None
		self.start_date = None
		self.end_date = None
		self.activities = None
		self.notes = None
		self.field_of_study = None

	@staticmethod
	def create(node):
		"""
		<educations total="">
		 <education>
		 <id>
		 <school-name>
		 <degree>
		 <start-date>
		 <year>
		 </start-date>
		 <end-date>
		 <year>
		 </end-date>
		 </education>
		</educations>
		"""
		children = node.getElementsByTagName("education")
		result = []
		for child in children:
			education = Education()
			education.id = str(education._get_child(child, "id"))
			#education.activities = str(education._get_child(child, "activities"))
			#education.notes = str(education._get_child(child, "notes"))
			education.school_name = str(education._get_child(child, "school-name"))
			education.degree = str(education._get_child(child, "degree"))
			education.field_of_study = str(education._get_child(child, "field-of-study"))
			
			start_date = child.getElementsByTagName("start-date")
			if start_date:
				start_date = start_date[0]
				try:
					education.start_date = int(education._get_child(start_date, "year"))
				except Exception:
					pass

			end_date = child.getElementsByTagName("end-date")
			if end_date:
				end_date = end_date[0]
				try:
					education.end_date = int(education._get_child(end_date, "year"))
				except Exception:
					pass

			result.append(education)            
		return result

	def _get_child(self, node, tagName):
		try:
			domNode = node.getElementsByTagName(tagName)[0]
			childNodes = domNode.childNodes
			if childNodes:
				return childNodes[0].nodeValue
			return None
		except:
			return None


class Position(object):
	# Class that wraps a business position info of a user
	def __init__(self):
		self.id = None
		self.title = None
		self.summary = None
		self.start_date = []
		self.end_date = []
		self.company = None
		self.companyID = None

	@staticmethod
	def create(node):
		"""
		<positions total='1'>
		 <position>
		 <id>101526695</id>
		 <title>Developer</title>
		 <summary></summary>
		 <start-date>
		  <year>2009</year>
		  <month>9</month>
		 </start-date>
		 <is-current>true</is-current>
		 <company>
		 <name>Akinon</name>
		 </company>
		 </position>
		</positions>
		"""
		children = node.getElementsByTagName("position")
		result = []
		for child in children:
			position = Position()
			position.id = str(position._get_child(child, "id"))
			position.title = str(position._get_child(child, "title"))
			position.summary = str(position._get_child(child, "summary"))
			
			company = child.getElementsByTagName("company")
			if company:
				company = company[0]
				position.company = str(position._get_child(company, "name"))
				try:
					position.companyID = str(position._get_child(company, "id"))
				except:
					pass

			start_date = child.getElementsByTagName("start-date")
			if start_date:
				start_date = start_date[0]
				try:
					year = int(position._get_child(start_date, "year"))
					position.start_date = [year, 1]
					month = int(position._get_child(start_date, "month"))
					position.start_date = [year, month]
				except Exception:
					pass

			end_date = child.getElementsByTagName("end-date")
			if end_date:
				end_date = end_date[0]
				try:
					year = int(position._get_child(end_date, "year"))
					position.end_date = [year, 1]
					month = int(position._get_child(end_date, "month"))
					position.end_date = [year, month]
				except Exception:
					pass

			result.append(position)

		return result

	def _get_child(self, node, tagName):
		try:
			domNode = node.getElementsByTagName(tagName)[0]
			childNodes = domNode.childNodes
			if childNodes:
				return childNodes[0].nodeValue
			return None
		except:
			return None

class Company(object):
	def __init__(self):
		self.id = None
		self.name = None
		self.universal_name = None
		self.ticker = None
		self.specialties = []
		self.industry = None
		self.company_type = None
		self.size = None
		self.hq = None
		self.otherLocations = []

	def __str__(self):
		temp = "id: " + self.id + "\n"
		temp = temp + "name: " + self.name + "\n"
		temp = temp + "universal-name: " + self.universal_name + "\n"
		temp = temp + "ticker: " + self.ticker + "\n"
		#temp = temp + "specialties: " + self.specialties + "\n"
		temp = temp + "industry: " + self.industry + "\n"
		temp = temp + "locations: " + self.locations + "\n"
		return temp

	@staticmethod
	def create(xml_string):
		try:
			print xml_string
			document = minidom.parseString(xml_string)
			company = document.getElementsByTagName("company")[0]
			companyObj = Company()
			companyObj.id = str(companyObj._get_child(company, "id"))
			companyObj.name = str(companyObj._get_child(company, "name"))
			companyObj.universal_name = str(companyObj._get_child(company, "universal-name"))
			companyObj.ticker = str(companyObj._get_child(company, "ticker"))
			companyObj.industry = str(companyObj._get_child(company, "industry"))
			
			cType = company.getElementsByTagName("company-type")
			if cType:
				companyObj.company_type = str(cType[0].getElementsByTagName("name")[0].firstChild.nodeValue)
				
			cSize = company.getElementsByTagName("employee-count-range")
			if cSize:
				companyObj.size = str(cSize[0].getElementsByTagName("name")[0].firstChild.nodeValue)
			
			specs = company.getElementsByTagName("specialties")
			if specs:
				specs = specs[0]
				specialts = specs.getElementsByTagName("specialty")
				for specialty in specialts:
					companyObj.specialties.append(str(specialty.firstChild.nodeValue))
			
			location = company.getElementsByTagName("locations")
			if location:
				location = location[0].getElementsByTagName("location")
				for loc in location:
					l = ''
					city = loc.getElementsByTagName("city")
					if city:
						try:
							city = str(city[0].firstChild.nodeValue)
							l = l + city + ','
						except:
							l = l + ','
					state = loc.getElementsByTagName("state")
					if state:
						try:
							state = str(state[0].firstChild.nodeValue)
							l = l + state + ','
						except:
							l = l + ','
					postal = loc.getElementsByTagName("postal-code")
					if postal:
						try:
							postal = str(postal[0].firstChild.nodeValue)
							l = l + postal + ','
						except:
							l = l + ','
					country = loc.getElementsByTagName("country-code")
					if country:
						try:
							country = str(country[0].firstChild.nodeValue)
							l = l + country
						except:
							pass
					if loc.getElementsByTagName("is-headquarters")[0].firstChild.nodeValue == 'true':
						companyObj.hq = l
					else:
						companyObj.otherLocations.append(l)
			#company.logo_url = company._get_child(company, "logo-url")
			#company.type = company._get_child(company, "type")
			return companyObj
		except:
			return None
		return None

	def _get_child(self, node, tagName):
		try:
			domNode = node.getElementsByTagName(tagName)[0]
			childNodes = domNode.childNodes
			if childNodes:
				return childNodes[0].nodeValue
			return None
		except:
			return None

class Profile(object):
	# Wraps the data which comes from Profile API of LinkedIn.
	def __init__(self):
		self.id = None
		self.first_name = None
		self.last_name = None
		self.location = None
		self.industry = None
		self.summary = None
		self.specialties = None
		self.interests = None
		self.honors = None
		self.positions = []
		self.educations = []
		self.public_url = None
		self.picture_url = None
		self.current_status = None
		self.skills = []
		self.languages = []
		self.date_of_birth = None
		self.api_request = None
		self.header_name = None
		self.header_value = None

	@staticmethod
	def create(xml_string):
		# This method is a static method so it shouldn't be called from an instance.
        # Parses the given xml string and results in a Profile instance.
        # If the given instance is not valid, this method returns NULL.
		profile = Profile()
		try:
			print xml_string # helps debug any time a field is empty
			document = minidom.parseString(xml_string)            
			person = document.getElementsByTagName("person")[0]
			profile.id = str(profile._get_child(person, "id"))
			#profile.first_name = str(profile._get_child(person, "first-name"))
			#profile.last_name = str(profile._get_child(person, "last-name"))
			#profile.headline = str(profile._get_child(person, "headline"))
			#profile.honors = str(profile._get_child(person, "honors"))
			#profile.summary = str(profile._get_child(person, "summary"))
			#profile.picture_url = profile._unescape(profile._get_child(person, "picture-url"))
			#profile.current_status = profile._get_child(person, "current-status")
			
			# specialties = profile._get_child(person, "specialties")
			# if specialties:
			# 	profile.specialties = str(specialties)
			# 
			# industry = profile._get_child(person, "industry")
			# if industry:
			# 	profile.industry = str(industry)
			
			interests = profile._get_child(person, "interests")
			print interests
			if interests:
				profile.interests = str(interests)

			lang = person.getElementsByTagName("languages")
			if lang:
				lang = lang[0]
				all_lang = lang.getElementsByTagName("name")
				for l in all_lang:
					profile.languages.append(str(l.firstChild.nodeValue))

			bday = person.getElementsByTagName("date-of-birth")
			if bday:
				bday = bday[0]
				profile.date_of_birth = int(profile._get_child(bday, "year"))

			sk = person.getElementsByTagName("skills")
			if sk:
				sk = sk[0]
				all_skills = sk.getElementsByTagName("name")
				for skill in all_skills:
					profile.skills.append(str(skill.firstChild.nodeValue))

			# get the profile URL
			public_url = person.getElementsByTagName("site-standard-profile-request")
			if public_url:
				public_url = public_url[0]
				profile.public_url = profile._get_child(public_url, "url")

			# create location
			location = person.getElementsByTagName("location")
			if location:
				location = location[0]
				profile.location = str(profile._get_child(location, "name"))

			# create public profile url
			public_profile = person.getElementsByTagName("site-public-profile-request")
			if public_profile:
				public_profile = public_profile[0]
				profile.public_url = profile._get_child(public_profile, "url")
			
			# create api standard profile request URL, this field allows you to get out-of-network profiles
			api_profile = person.getElementsByTagName("api-standard-profile-request")
			if api_profile:
				api_profile = api_profile[0]
				profile.api_request = profile._get_child(api_profile, "url")
				profile.header_name = api_profile.getElementsByTagName("name")[0].firstChild.nodeValue
				profile.header_value = api_profile.getElementsByTagName("value")[0].firstChild.nodeValue

			# create positions
			positions = person.getElementsByTagName("positions")
			if positions:
				positions = positions[0]
				profile.positions = Position.create(positions)

			# create educations
			educations = person.getElementsByTagName("educations")
			if educations:
				educations = educations[0]
				profile.educations = Education.create(educations)

			return profile
		except:
			return profile

		return None

	def _unescape(self, url):
		if url:
			return unescape(url)
		return url

	def _get_child(self, node, tagName):
		try:
			if tagName == "summary":
				for n in node.getElementsByTagName(tagName):
					if n.parentNode.tagName == node.tagName:
						domNode = n
						break
			else:
				domNode = node.getElementsByTagName(tagName)[0]

			if domNode.parentNode.tagName == node.tagName:
				childNodes = domNode.childNodes
				if childNodes:
					return childNodes[0].nodeValue
				return None
			else:
				return None
		except:
			return None

class ConnectionError(Exception):
	pass

class LinkedIn(object):
	
	def __init__(self):
		# Set up for the API
		self.consumer_key = 'k1tofeoqr4id'
		self.consumer_secret = 'KgEvtAPuvFCj1FoE'
		request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
		authorize_url = 'https://api.linkedin.com/uas/oauth/authorize'
		access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
		
		# Set up instances of our Token and Consumer. The Consumer.key and 
		# Consumer.secret are given to you by the API provider. The Token.key and
		# Token.secret is given to you after a three-legged authentication.
		consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
		client = oauth.Client(consumer)

		resp, content = client.request(request_token_url, "POST")
		if resp['status'] != '200':
			raise Exception("Invalid response %s." % resp['status'])

		self.request_token = dict(urlparse.parse_qsl(content))

		print "Request Token:"
		print " - oauth_token = %s" % self.request_token['oauth_token']
		print " - oauth_token_secret = %s" % self.request_token['oauth_token_secret']
		print
		print "Go to the following link in your browser:"
		print "%s?oauth_token=%s" % (authorize_url, self.request_token['oauth_token'])
		print
		oauth_verifier = raw_input('What is the PIN? ')

		self.token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
		self.token.set_verifier(oauth_verifier)
		client = oauth.Client(consumer, self.token)

		resp, content = client.request(access_token_url, "POST")
		self.access_token = dict(urlparse.parse_qsl(content))
		
		# keep track of the number of API calls, throttle limits
		self.get_profile_api_calls = 0
		self.profile_search_api_calls = 0
		
		self.get_company_api_calls = 0
		self.company_search_api_calls = 0
		
		return
	
	# retrieves the profile
	def get_profile(self, member_id = None):
		# get own profile by default
		if member_id is None:
			url = "http://api.linkedin.com/v1/people/~:(id)"
			content = self.req_content(url)
			member_id = Profile.create(content).id
		
		url = "http://api.linkedin.com/v1/people/id=" + member_id
		fields = ":(id,first-name,last-name,date-of-birth,educations,skills,interests,languages,location,positions,api-standard-profile-request)"
		self.get_profile_api_calls = self.get_profile_api_calls + 1
		content = self.req_content(url + fields)
		
		#
		if content:
			return Profile.create(content)
		else:
			return self.get_profile_OON(member_id)
	
	def get_interests(self, member_id = None):
		url = 'http://api.linkedin.com/v1/people/' + member_id
		fields = ':(id,api-standard-profile-request)'
		self.get_profile_api_calls = self.get_profile_api_calls + 1
		content = self.req_content(url + fields)
		
		document = minidom.parseString(content)
		header_name = document.getElementsByTagName("api-standard-profile-request")[0].getElementsByTagName("name")[0].firstChild.nodeValue
		header_value = document.getElementsByTagName("api-standard-profile-request")[0].getElementsByTagName("value")[0].firstChild.nodeValue
		fields = ":(id,interests)"
		self.get_profile_api_calls = self.get_profile_api_calls + 1
		content = self.req_content(url + fields, header_name, header_value)
		return Profile.create(content)
	
	# retrieves company profile
	def get_company(self, company_id):
		url = "http://api.linkedin.com/v1/companies/" + company_id
		fields = ":(id,name,universal-name,ticker,specialties,industry,company-type,employee-count-range,locations:(is-headquarters,description,address:(country-code,state,city,postal-code)))"
		self.get_company_api_calls = self.get_company_api_calls + 1
		content = self.req_content(url + fields)
		return Company.create(content)
	
	# searches for profiles that fit params, ex: parameters = 'company-name=google&count=3'
	def profile_search(self, params):
		url = 'http://api.linkedin.com/v1/people-search'
		fields = ':(people:(id,first-name,last-name,api-standard-profile-request),num-results)'
		param = '?' + params
		self.profile_search_api_calls = self.profile_search_api_calls + 1
		content = self.req_content(url + fields + param)
		print content
		# parsing the results into list of profiles
		if content:
			document = minidom.parseString(content)
			people = document.getElementsByTagName("person")
			result = []
			for person in people:
				profile = Profile.create(person.toxml())
				print profile
				if profile is not None:
					result.append(profile)
			return result
		else:
			return None
	
	# returns the num-results from a profile search
	def num_profiles(self, params):
		url = 'http://api.linkedin.com/v1/people-search'
		fields = ':(people:(id,first-name,last-name,api-standard-profile-request),num-results)'
		param = '?' + params
		
		content = self.req_content(url + fields + param)
		print content
		
		if content:
			document = minidom.parseString(content)
			num = document.getElementsByTagName("num-results")
			if num:
				return str(num[0].firstChild.nodeValue)
		else:
			return None
	
	# searches for companies that fit params, ex: 'company-name=' + company
	def company_search(self, params):
		url = 'http://api.linkedin.com/v1/company-search/'
		param = '?' + str(params)
		self.company_search_api_calls = self.company_search_api_calls + 1
		content = self.req_content(url + param)
		
		# parsing the results into list of companies
		if content:
			document = minidom.parseString(content)
			companies = document.getElementsByTagName("company")
			result = []
			for company in companies:
				cProfile = Company.create(company.toxml())
				print cProfile
				if cProfile is not None:
					result.append(cProfile)
			return result
		else:
			return None
		
	def get_profile_OON(self, member_id):
		url = 'http://api.linkedin.com/v1/people/' + member_id
		fields = ':(id,api-standard-profile-request)'
		self.get_profile_api_calls = self.get_profile_api_calls + 1
		content = self.req_content(url + fields)
		
		document = minidom.parseString(content)
		header_name = document.getElementsByTagName("api-standard-profile-request")[0].getElementsByTagName("name")[0].firstChild.nodeValue
		header_value = document.getElementsByTagName("api-standard-profile-request")[0].getElementsByTagName("value")[0].firstChild.nodeValue
		fields = ":(id,date-of-birth,educations,skills,interests,languages,location,positions,api-standard-profile-request)"
		self.get_profile_api_calls = self.get_profile_api_calls + 1
		content = self.req_content(url + fields, header_name, header_value)
		return Profile.create(content)
	
	# prints out the number of various API calls made
	def print_api_calls(self):
		print 'get_profile API calls: ' + str(self.get_profile_api_calls)
		print 'profile_search API calls: ' + str(self.profile_search_api_calls)
		print 'get_company API calls: ' + str(self.get_company_api_calls)
		print 'company_search API calls: ' + str(self.company_search_api_calls)
	
	# makes the API actual call with tokens and stuff
	def req_content(self, url, header_name = None, header_value = None):
		consumer = oauth.Consumer(key = self.consumer_key, secret = self.consumer_secret)
		token = oauth.Token(key = self.access_token['oauth_token'], secret = self.access_token['oauth_token_secret'])
		client = oauth.Client(consumer, token)
		
		# API call
		if header_name is None and header_value is None:
			resp, content = client.request(url)
		else:
			resp, content = client.request(url, headers = {header_name:header_value})
		
		if resp['status'] == '200':
			print resp
			return content
		else:
			print "error"
			print resp
			print content
			self.print_api_calls()
			print url
			return None