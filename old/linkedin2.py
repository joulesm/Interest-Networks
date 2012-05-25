# utf-8

__version__ = "1.9"

# Provides a Pure Python LinkedIn API Interface.

try:
	import sha
except DeprecationWarning, derr:
	import hashlib
	sha = hashlib.sha1

import urllib, time, random, httplib, hmac, binascii, cgi, string, datetime
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
		try:
			print xml_string # helps debug any time a field is empty
			document = minidom.parseString(xml_string)            
			person = document.getElementsByTagName("person")[0]
			profile = Profile()
			profile.id = str(profile._get_child(person, "id"))
			#profile.first_name = str(profile._get_child(person, "first-name"))
			#profile.last_name = str(profile._get_child(person, "last-name"))
			#profile.headline = str(profile._get_child(person, "headline"))
			profile.specialties = str(profile._get_child(person, "specialties"))
			profile.industry = str(profile._get_child(person, "industry"))
			#profile.honors = str(profile._get_child(person, "honors"))
			profile.interests = str(profile._get_child(person, "interests"))
			#profile.summary = str(profile._get_child(person, "summary"))
			#profile.picture_url = profile._unescape(profile._get_child(person, "picture-url"))
			#profile.current_status = profile._get_child(person, "current-status")

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
			return None

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
	def __init__(self, api_key, api_secret, callback_url, gae = False):
		"""
		LinkedIn Base class that simply implements LinkedIn OAuth Authorization and LinkedIn APIs such as Profile, Connection vs.

		@ LinkedIn OAuth Authorization:
		In OAuth terminology, there are 2 tokens that we need in order to have permission to perform an API request. Those are request_token and access_token. Thus, this class basicly intends to wrap methods of OAuth spec. which are related of gettting request_token and access_token strings.

		@ Important Note:
		HMAC-SHA1 hashing algorithm will be used while encrypting a request body of an HTTP request. Other alternatives such as 'SHA-1' or 'PLAINTEXT' are ignored.

		@ Reference for OAuth:
		Please take a look at the link below if you have a basic knowledge of HTTP protocol
		http://developer.linkedin.com/docs/DOC-1008

		Please create an application from the link below if you do not have an API key and secret key yet.
		https://www.linkedin.com/secure/developer
		@api_key:    Your API key
		@api_secret: Your API secret key
		@callback_url: the return url when the user grants permission to Consumer.
		"""
		# Credientials
		self.API_ENDPOINT = "api.linkedin.com"
		self.BASE_URL = "https://%s" % self.API_ENDPOINT
		self.VERSION = "1.0"
		self._api_key = api_key
		self._api_secret = api_secret
		self._callback_url = callback_url
		self._gae = gae # Is it google app engine
		self._request_token = None # that comes later
		self._access_token = None # that comes later and later
		self._request_token_secret = None
		self._access_token_secret = None
		self._verifier = None
		self._error = None

	def request_token(self):
		"""
		Performs the corresponding API which returns the request token in a query string
		The POST Querydict must include the following:
		* oauth_callback
		* oauth_consumer_key
		* oauth_nonce
		* oauth_signature_method
		* oauth_timestamp
		* oauth_version
		"""
		self.clear()

		method = "GET"
		relative_url = "/uas/oauth/requestToken"

		query_dict = self._query_dict({"oauth_callback" : self._callback_url})

		self._calc_signature(self._get_url(relative_url), query_dict, self._request_token_secret, method)

		try:
			response = self._https_connection(method, relative_url, query_dict)
		except ConnectionError:
			return False

		oauth_problem = self._get_value_from_raw_qs("oauth_problem", response)
		if oauth_problem:
			self._error = oauth_problem
			return False

		self._request_token = self._get_value_from_raw_qs("oauth_token", response)
		self._request_token_secret = self._get_value_from_raw_qs("oauth_token_secret", response)
		return True

	def access_token(self, request_token = None, request_token_secret = None, verifier = None):
		"""
		Performs the corresponding API which returns the access token in a query string
		According to the link (http://developer.linkedin.com/docs/DOC-1008), POST Querydict must include the following:
		* oauth_consumer_key
		* oauth_nonce
		* oauth_signature_method
		* oauth_timestamp
		* oauth_token (request token)
		* oauth_version
		"""
		self._request_token = request_token and request_token or self._request_token
		self._request_token_secret = request_token_secret and request_token_secret or self._request_token_secret
		self._verifier = verifier and verifier or self._verifier
		# if there is no request token, fail immediately
		if self._request_token is None:
			raise OAuthError("There is no Request Token. Please perform 'request_token' method and obtain that token first.")

		if self._request_token_secret is None:
			raise OAuthError("There is no Request Token Secret. Please perform 'request_token' method and obtain that token first.")

		if self._verifier is None:
			raise OAuthError("There is no Verifier Key. Please perform 'request_token' method, redirect user to API authorize page and get the _verifier.")

		method = "GET"
		relative_url = "/uas/oauth/accessToken"
		query_dict = self._query_dict({
					"oauth_token" : self._request_token,
					"oauth_verifier" : self._verifier
					})

		self._calc_signature(self._get_url(relative_url), query_dict, self._request_token_secret, method)

		try:
			response = self._https_connection(method, relative_url, query_dict)
		except ConnectionError:
			return False

		oauth_problem = self._get_value_from_raw_qs("oauth_problem", response)
		if oauth_problem:
			self._error = oauth_problem
			return False

		self._access_token = self._get_value_from_raw_qs("oauth_token", response)
		self._access_token_secret = self._get_value_from_raw_qs("oauth_token_secret", response)
		return True

	def get_profile(self, member_id = None, url = None, fields=['id', 'date-of-birth', 'educations', 'skills', 'interests', 'languages', 'location', 'positions', 'api-standard-profile-request']):
		"""
		Gets the public profile for a specific user. It is determined by his/her member id or public url.
		If none of them are given, current user's details are fetched.
		The argument 'fields' determines how much information will be fetched.

		Examples:
		client.get_profile(merber_id = 123, url = None, fields=['first-name', 'last-name']) : fetches the profile of a user whose id is 123. 

		client.get_profile(merber_id = None, url = None, fields=['first-name', 'last-name']) : fetches current user's profile

		client.get_profile(member_id = None, 'http://www.linkedin.com/in/ozgurv') : fetches the profile of a  user whose profile url is http://www.linkedin.com/in/ozgurv

		@ Returns Profile instance
		"""
		# if there is no access token or secret, fail immediately
		self._check_tokens()

		# specify the url according to the parameters given
		raw_url = "/v1/people/"
		if url:
			url = self._quote(url)
			#raw_url = (raw_url + "url=%s:public") % url
			raw_url = (raw_url + "url=%s") % url
			print raw_url
		elif member_id:
			raw_url = (raw_url + "id=%s" % member_id)
		else:
			raw_url = raw_url + "~"
		#if url is None:
		if True:
			fields = ":(%s)" % ",".join(fields) if len(fields) > 0 else None
			if fields:
				raw_url = raw_url + fields

		try:
			response = self._do_normal_query(raw_url)
			return Profile.create(response) # this creates Profile instance or gives you null
		except ConnectionError:
			return None
			
		return
	
	# this method is for profiles that are Out Of Network.
	def get_profile_OON(self, member_id):
		profile = self.get_profile(member_id = member_id, fields=['id','api-standard-profile-request'])
		print profile.id
		print profile.header_name
		print profile.header_value
		
		raw_url = "/v1/people/"
		raw_url = (raw_url + "%s" % member_id)
		
		try:
			response = self._do_OON_query(raw_url, profile)
			return Profile.create(response)
		except ConnectionError:
			return None
		
		return

	def get_company(self, id):
		# if there is no access token or secret, fail immediately
		self._check_tokens()

		# specify the url according to the parameters given
		raw_url = "/v1/companies/" + id

		fields = ['id', 'name', 'universal-name', 'ticker', 'specialties', 'industry', 'company-type', 'employee-count-range', 'locations:(is-headquarters,description,address:(country-code,state,city,postal-code))']
		fields = ":(%s)" % ",".join(fields) if len(fields) > 0 else None
		raw_url = raw_url + fields

		try:
			response = self._do_normal_query(raw_url)
			return Company.create(response) # this creates Profile instance or gives you null
		except ConnectionError:
			return None

	def get_connections(self, member_id = None, public_url = None, fields=[]):
		"""
		Fetches the connections of a user whose id is the given member_id or url is the given public_url
		If none of the parameters given, the connections of the current user are fetched.
		@Returns: a list of Profile instances or an empty list if there is no connection.

		Example urls:
		* http://api.linkedin.com/v1/people/~/connections (for current user)
		* http://api.linkedin.com/v1/people/id=12345/connections (fetch with member_id)
		* http://api.linkedin.com/v1/people/url=http%3A%2F%2Fwww.linkedin.com%2Fin%2Flbeebe/connections (fetch with public_url)
		"""
		self._check_tokens()

		raw_url = "/v1/people/%s/connections"
		if member_id:
			raw_url = raw_url % ("id=" + member_id)
		elif public_url:
			raw_url = raw_url % ("url=" + self._quote(public_url))
		else:
			raw_url = raw_url % "~"
		fields = ":(%s)" % ",".join(fields) if len(fields) > 0 else None
		if fields:
			raw_url = raw_url + fields

		try:
			response = self._do_normal_query(raw_url)
			document = minidom.parseString(response)
			connections = document.getElementsByTagName("person")
			result = []
			for connection in connections:
				profile = Profile.create(connection.toxml())
				if profile is not None:
					result.append(profile)

			return result
		except ConnectionError:
			return None

	def get_search(self, parameters, fields=None):
		"""
		Use the Search API to find LinkedIn profiles using keywords,
		company, name, or other methods. This returns search results,
		which are an array of matching member profiles. Each matching
		profile is similar to a mini-profile popup view of LinkedIn
		member profiles.

		Request URL Structure:
		http://api.linkedin.com/v1/people?keywords=['+' delimited keywords]&name=[first name + last name]&company=[company name]&current-company=[true|false]&title=[title]&current-title=[true|false]&industry-code=[industry code]&search-location-type=[I,Y]&country-code=[country code]&postal-code=[postal code]&network=[in|out]&start=[number]&count=[1-10]&sort-criteria=[ctx|endorsers|distance|relevance]
		"""
		self._check_tokens()
		
		raw_url = "/v1/people-search"
		fields = ":(people:(id,first-name,last-name,api-standard-profile-request),num-results)"
		#fields = ":(%s)" % ",".join(fields) if len(fields) > 0 else None
		#if fields:
		#	raw_url = raw_url + fields
		raw_url = raw_url + fields

		try:
			response = self._do_normal_query(raw_url, method="GET", params=parameters)
		except ConnectionError:
			return None

		error = self._parse_error(response)
		if error:
			self._error = error
			return None

		print response
		document = minidom.parseString(response)
		connections = document.getElementsByTagName("person")
		result = []
		for connection in connections:
			profile = Profile.create(connection.toxml())
			print profile
			if profile is not None:
				result.append(profile)
		return result

	# parameters = {'keywords': 'google'}
	def company_search(self, parameters):
		self._check_tokens()

		try:
			response = self._do_normal_query("/v1/company-search", method="GET", params=parameters)
		except ConnectionError:
			return None
		error = self._parse_error(response)
		if error:
			self._error = error
			return None
		document = minidom.parseString(response)
		companies = document.getElementsByTagName("company")
		result = []
		for company in companies:
			tempcompany = Company.create(company.toxml())
			if tempcompany is not None:
				result.append(tempcompany)
		return result

	def get_authorize_url(self, request_token = None):
		self._request_token = request_token and request_token or self._request_token
		if self._request_token is None:
			raise OAuthError("OAuth Request Token is NULL. Plase acquire this first.")
		return "%s%s?oauth_token=%s" % (self.BASE_URL, "/uas/oauth/authorize", self._request_token)

	def get_error(self):
		return self._error

	def clear(self):
		self._request_token = None
		self._access_token = None
		self._verifier = None
		self._request_token_secret = None
		self._access_token_secret = None
		self._error = None

	#################################################
	# HELPER FUNCTIONS                              #
	# You do not explicitly use those methods below #
	#################################################

	def _generate_nonce(self, length = 20):
		return ''.join([string.letters[random.randint(0, len(string.letters) - 1)] for i in range(length)])

	def _get_url(self, relative_path):
		return self.BASE_URL + relative_path

	def _generate_timestamp(self):
		return str(int(time.time()))

	def _quote(self, st):
		return urllib.quote(st, safe='~')

	def _utf8(self, st):
		return isinstance(st, unicode) and st.encode("utf-8") or str(st)

	def _urlencode(self, query_dict):
		keys_and_values = [(self._quote(self._utf8(k)), self._quote(self._utf8(v))) for k,v in query_dict.items()]
		keys_and_values.sort()
		return '&'.join(['%s=%s' % (k, v) for k, v in keys_and_values])

	def _get_value_from_raw_qs(self, key, qs):
		raw_qs = cgi.parse_qs(qs, keep_blank_values = False)
		rs = raw_qs.get(key)
		if type(rs) == list:
			return rs[0]
		else:
			return rs

	def _signature_base_string(self, method, uri, query_dict):
		return "&".join([self._quote(method), self._quote(uri), self._quote(self._urlencode(query_dict))])

	def _parse_error(self, str_as_xml):
		"""
		Helper function in order to get _error message from an xml string.
		In coming xml can be like this:
		<?xml VERSION='1.0' encoding='UTF-8' standalone='yes'?>
		<_error>
		 <status>404</status>
		 <timestamp>1262186271064</timestamp>
		 <_error-code>0000</_error-code>
		 <message>[invalid.property.name]. Couldn't find property with name: first_name</message>
		</_error>
		"""
		try:
			xmlDocument = minidom.parseString(str_as_xml)
			#if len(xmlDocument.getElementsByTagName("_error")) > 0: 
			if len(xmlDocument.getElementsByTagName("error")) > 0: 
				error = xmlDocument.getElementsByTagName("message")
				if error:
					error = error[0]
					return error.childNodes[0].nodeValue
			return None
		except Exception, detail:
			raise OAuthError("Invalid XML String given: error: %s" % repr(detail))

	def _create_oauth_header(self, query_dict):
		header = 'OAuth realm="http://api.linkedin.com", '
		header += ", ".join(['%s="%s"' % (k, self._quote(query_dict[k])) for k in sorted(query_dict)])
		print header
		return header

	def _query_dict(self, additional = {}):
		query_dict = {"oauth_consumer_key": self._api_key,
						"oauth_nonce": self._generate_nonce(),
						"oauth_signature_method": "HMAC-SHA1",
						"oauth_timestamp": self._generate_timestamp(),
						"oauth_version": self.VERSION
						}
		query_dict.update(additional)
		return query_dict

	def _do_normal_query(self, relative_url, body=None, method="GET", params=None):
		method = method
		query_dict = self._query_dict({"oauth_token" : self._access_token})
		signature_dict = dict(query_dict)
		if (params):
			signature_dict.update(params)

		query_dict["oauth_signature"] = self._calc_signature(self._get_url(relative_url),
										signature_dict, self._access_token_secret, method, update=False)
		if (params):
			relative_url = "%s?%s" % (relative_url, self._urlencode(params))
		response = self._https_connection(method, relative_url, query_dict, body)
		if (response):
			error = self._parse_error(response)
			if error:
				self._error = error
				print error
				raise ConnectionError()
		return response
	
	# special headers for Out Of Network calls
	def _do_OON_query(self, relative_url, profile, body=None, method="get", params=None):
		query_dict = self._query_dict({"oauth_token" : self._access_token})
		signature_dict = dict(query_dict)
		if (params):
			signature_dict.update(params)
		query_dict["oauth_signature"] = self._calc_signature(self._get_url(relative_url),
										signature_dict, self._access_token_secret, method, update=False)
		if (params):
			relative_url = "%s?%s" % (relative_url, self._urlencode(params))
		response = self._OON_https_connection(method, relative_url, query_dict, profile, body)
		if (response):
			error = self._parse_error(response)
			print response
			if error:
				self._error = error
				print "here2"
				print error
				raise ConnectionError()
				print "here3"
		return response
	
	def _OON_https_connection(self, method, relative_url, query_dict, profile, body=None):
		name = self._utf8(profile.header_name)
		#value = "name-search:" + profile.header_value[-4:]
		value = self._utf8(profile.header_value)
		print name
		print value
		header = self._create_oauth_header(query_dict)
		connection = None
		try:
			print relative_url
			connection = httplib.HTTPSConnection(self.API_ENDPOINT)
			connection.request(method, relative_url, body = body,
								headers={'Authorization':header, name:value})
			response = connection.getresponse()
			if response is None:
				self._error = "No HTTP response received."
				raise ConnectionError()
			return response.read()
		finally:
			if (connection):
				connection.close()
		return
	
	def _check_tokens(self):
		if self._access_token is None:
			self._error = "There is no Access Token. Please perform 'access_token' method and obtain that token first."
			raise OAuthError(self._error)
		if self._access_token_secret is None:
			self._error = "There is no Access Token Secret. Please perform 'access_token' method and obtain that token first."
			raise OAuthError(self._error)

	def _calc_key(self, token_secret):
		key = self._quote(self._api_secret) + "&"
		if (token_secret):
			key += self._quote(token_secret)
		return key

	def _calc_signature(self, url, query_dict, token_secret, method = "GET", update=True):
		query_string = self._quote(self._urlencode(query_dict))
		signature_base_string = "&".join([self._quote(method), self._quote(url), query_string])
		hashed = hmac.new(self._calc_key(token_secret), signature_base_string, sha)
		signature = binascii.b2a_base64(hashed.digest())[:-1]
		if (update):
			query_dict["oauth_signature"] = signature
		return signature

	def _https_connection(self, method, relative_url, query_dict, body=None):
		header = self._create_oauth_header(query_dict)
		connection = None
		try:
			print relative_url
			connection = httplib.HTTPSConnection(self.API_ENDPOINT)
			connection.request(method, relative_url, body = body,
								headers={'Authorization':header})
			response = connection.getresponse()
			if response is None:
				self._error = "No HTTP response received."
				raise ConnectionError()
			return response.read()
		finally:
			if (connection):
				connection.close()
		return

	########################
	# END HELPER FUNCTIONS #
	########################