import linkedin3
import helper as h
import json
import sys
import string

api = linkedin3.LinkedIn()

######################

# This section searched the IDs for all ML companies and saved to file. Two companies were not found: "Culture Convenience Club" and "Nul-G"
# searchList = h.readFile('MLcompanies.txt')
# ML_IDs = []
# no_search = []
# for company in searchList:
# 	search = api.company_search({'keywords': company, 'count': 1})
# 	if search:
# 		ML_IDs.append([company, search[0].name, search[0].id])
# 	else:
# 		no_search.append(company)
# 
# h.saveFile(ML_IDs, 'ML_IDs.txt')
# print "no search results for: "
# for i in no_search:
# 	print i

# This section pulls all the company profiles for the ML companies and saves as JSON
# temp = h.readFile('ML_IDs.txt')
# ML_IDs = []
# for ML in temp:
# 	ML = ML.replace('[','').replace(']','').replace('u\'','').replace('\'','').split(',')
# 	ML[2] = str(int(ML[2]))
# 	ML_IDs.append(ML)
# ML_comp_profiles = []
# for company in ML_IDs:
# 	ML_comp_profiles.append(h.JSONifyCompany(api.get_company(company[2])))
# 
# with open('ML_comp_profiles.txt', 'w') as f:
# 	f.write(json.dumps(ML_comp_profiles))

# This section pulls as many profileIDs as possible for each companyID
#cIDs = json.loads(open('ML_public_comps.py', 'r').read())
#cIDs2 = cIDs[0:14] # Mar 4, 7pm with mine. Saved as IDs_hasbro_emc, size 9601
#cIDs2 = cIDs[14:28]	# Mar 6, 3pm with Eyal. Saved as IDs_espn_timewarner, size 1503
#cIDs2 = cIDs[28:42]	# Mar 6, 3pm with mine. Saved as IDs_verizon_sun, size 8226
#cIDs2 = cIDs[42:]		# Mar 6, 4pm with Elisha. Saved as IDs_telecomitalia_volkswagen, len 324
#h.getPIDsFromCIDs(api, cIDs2)
# Mar 6, 4pm, combined all IDs into one file called IDs_all.txt, len 19654

# making a new file with just the IDs
profs = json.loads(open('profiles.json','r').read())
IDs = []
for prof in profs:
	IDs.append(prof['id'])

cIDs = json.loads(open('ML_public_comps_no_num.py', 'r').read())
cIDs = cIDs[:] # Mar 20, 5pm with mine
cIDs = cIDs[13:]	# Mar 20, 5pm with Eyal
cIDs = cIDs[29:]	# Mar 20, 11pm with mine
for cID in cIDs:
	cID['numIDs'] = str(h.countCIDs(api, cID, IDs))
	with open('ML_public_comps.py', 'a') as f:
		f.write(json.dumps(cID) + ',\n')
# saved as ML_public_comps.py

pIDs = h.readFile('./IDs_all.txt')
#pIDs2 = pIDs[0:845]	# Mar 4, 7pm with mine. Saved as profiles_0_845, size 725
#pIDs2 = pIDs[845:]		# Mar 5, 2pm with Eyal, saved as profiles_0_1083, size 927
#pIDs2 = pIDs[1083:]	# Mar 5, 3pm with Elisha, saved as profiles_0_1645, size 1458
#pIDs2 = pIDs[1645:]	# Mar 5, 4pm with Karthik, saved as profiles_0_1869, size 1639

#pIDs2 = pIDs[1870:]	# Mar 6, 3pm with Elisha, saved as profiles_0_2620, size 2391
#pIDs2 = pIDs[2621:]	# Mar 6, 4pm with Dawei, saved as profiles_0_3624, size 3395
#pIDs2 = pIDs[3625:]	# Mar 6, 4pm with Dan, saved as profiles_0_4872, size 4643
#pIDs2 = pIDs[4873:]	# Mar 6, 5pm with Kevin, saved as profiles_0_4972, ID4973 is bad
#pIDs2 = pIDs[4974:]	# continue with Kevin, saved as profiles_0_5040, internal error
#pIDs2 = pIDs[5041:]	# continue with Kevin, saved as profiles_0_5130, internal error
#pIDs2 = pIDs[5131:]	# continue with Kevin, saved as profiles_0_5334, internal error
#pIDs2 = pIDs[5335:]	# continue with Kevin, saved as profiles_0_5362, internal error
#pIDs2 = pIDs[5363:]	# continue with Kevin, saved as profiles_0_5626, size 5423
#pIDs2 = pIDs[5627:]	# Mar 6, 6pm with Eyal, saved as profiles_0_5677, internal error
#pIDs2 = pIDs[5678:]	# continue with Eyal, saved as profiles_0_5840, internal error
#pIDs2 = pIDs[5841:]	# continue with Eyal, saved as profiles_0_6080, internal error
#pIDs2 = pIDs[6081:]	# continue with Eyal, saved as profiles_0_6159, internal error
#pIDs2 = pIDs[6160:]	# continue with Eyal, saved as profiles_0_6321

#pIDs2 = pIDs[6322:]	# Mar 6, 7pm with mine, saved as profiles_0_6584, new day
#pIDs2 = pIDs[6585:]	# continue with mine, saved as profiles_0_7468, size 7265
#pIDs2 = pIDs[7469:]	# Mar 6, 11pm with Dan, saved as profiles_0_8236
#pIDs2 = pIDs[8237:]	# continue with Dan, saved as profiles_0_8489, size 8286
#pIDs2 = pIDs[8490:]	# Mar 6, 11pm with Eyal, saved as profiles_0_9536
#pIDs2 = pIDs[9537:]	# Mar 6, 11pm with Tam, saved as profiles_0_9730
#pIDs2 = pIDs[9731:]	# Mar 7, 1pm with Kevin, saved as profiles_0_10420 #9731-10420 is twice
#pIDs2 = pIDs[10421:]	# Mar 7, 1pm with Pol, internal error
#pIDs2 = pIDs[10655:]	# continue with Pol, saved as profiles_0_11579
#pIDs2 = pIDs[11580:]	# Mar 7, 2pm with Travis, internal error
#pIDs2 = pIDs[11658:]	# continue with Travis, internal error, saved as profiles_0_11821
#pIDs2 = pIDs[11822:]	# Mar 7, 3pm with Dawei
#pIDs2 = pIDs[12600:]	# continue with Dawei, internal error, saved as 12644
#pIDs2 = pIDs[12645:]	# Mar 7, 4pm with Hoda, internal error
#pIDs2 = pIDs[12808:]	# continue with Hoda, saved as 13447
#pIDs2 = pIDs[13448:]	# Mar 7, 5pm with Xiao, internal error
#pIDs2 = pIDs[14108:]	# continue with Xiao, saved as 14421
#pIDs2 = pIDs[14422:]	# Mar 7, 5pm with Elisha, internal error
#pIDs2 = pIDs[14636:]	# continue with Elisha
#pIDs2 = pIDs[14665:]	# continue with Elisha, saved as 15092, size 15578!?!??!?

#pIDs2 = pIDs[15093:]	# Mar 7, 11pm with Tam, 15776
#pIDs2 = pIDs[15777:]	# Mar 7, 11pm with Dan, 16625
#pIDs2 = pIDs[16626:]	# Mar 7, 11pm with Kevin, 17297
#pIDs2 = pIDs[17298:]	# Mar 7, 11pm with Pol, 18221, size 18709????
#pIDs2 = pIDs[18222:]	# Mar 8, 11am with Travis, 19033
#pIDs2 = pIDs[19034:]	# Mar 8, 12pm with Dawei, 19220
#pIDs2 = pIDs[19221:]	# finished. saved as profiles_all.json, size 20138???!?
#len(pIDs) = 19654
# for ID in pIDs2:
# 	prof = api.get_profile(ID)
# 	if prof:
# 		h.saveProfile(prof)
# 
# # removing duplicate profiles
# profs = json.loads(open('profiles_all.json', 'r').read())
# 
# for i in range(len(profs)):
# 	if str(profs[i]['id']) == '1LUl-lRvaO':
# 		print i
# 	if str(profs[i]['id']) == 'hYh34jxfUA':
# 		print i
# # duplicate entries: 9527 to 10214 same as 10215 to 10902, duplicated 688 items
# a = profs[0:10215]
# b = profs[10903:]
# c = a + b
# # end size 19450
# for prof in c:
# 	with open('./profiles.json', 'a') as f:
# 		f.write(json.dumps(prof) + ',\n')

# finding all the empty profiles
for i in range(len(profs)):
	if profs[i]["id"] == None:
		print i
# print i
# 5974
# 6074
# 6110
# 6955
# 7678
# 8284
# 9247
# 13106
# 13240
# 13274
# 13324
# 16420
# 16421
# 18133
# write to profiles.json, len is 19436 (old is renamed to profiles_null)

# duplicate profile check
dups = []
for i in range(len(profs)):
	print i
	for j in range(i):
		if profs[i] == profs[j]:
			dups.append([i, j])
# len(dups) = 88
# dups = [[2019, 651], [3921, 1991], [5131, 5103], [5132, 5104], [5133, 5105], [5134, 5106], [5135, 5107], [5136, 5108], [5137, 5109], [5138, 5110], [5139, 5111], [5140, 5112], [5141, 5113], [5142, 5114], [5143, 5115], [5144, 5116], [5145, 5117], [5146, 5118], [5147, 5119], [5148, 5120], [5149, 5121], [5150, 5122], [5151, 5123], [5152, 5124], [5153, 5125], [5154, 5126], [5155, 5127], [5156, 5128], [5157, 5129], [5158, 5130], [6751, 2000], [6758, 642], [6762, 617], [7360, 6736], [7366, 4712], [7379, 2029], [8020, 6730], [8022, 2000], [8022, 6751], [8757, 2023], [9613, 1969], [9717, 637], [9974, 4716], [10154, 6769], [10477, 9935], [10548, 6737], [10814, 10342], [10842, 4431], [10852, 10536], [10883, 4020], [10916, 10914], [10917, 10915], [10944, 7361], [11014, 6266], [11707, 11706], [12054, 12053], [12103, 12102], [12173, 3335], [12676, 10535], [12980, 6663], [12998, 10939], [13007, 642], [13007, 6758], [13008, 4728], [13776, 10557], [13872, 4685], [13924, 8738], [13942, 605], [14008, 646], [14075, 2035], [14087, 607], [14341, 634], [14345, 665], [15230, 10333], [15231, 624], [15632, 6718], [15641, 633], [15642, 13905], [15671, 6783], [15679, 6093], [15682, 14090], [15705, 8736], [15711, 6748], [15714, 15660], [16392, 15356], [18080, 13876], [18090, 8746], [18092, 2017]]
# ensuring profiles are actually duplicates
for i in range(len(dups)):
	if profs[dups[i][0]] != profs[dups[i][1]]:
		print str(i) + ': ' + str(dups[i][0]) + ', ' + str(dups[i][1])
# 44: [10477, 9935]. 9935 is not a full profile
profs.pop(9935)	# this pop requires us to redo the duplicate check
dups.reverse()	# popping from the end doesn't mess with indices
remove = []
for i in range(len(dups)):	# getting only the 2nd duplicate
	remove.append(dups[i][0])
for i in range(len(remove) - 1):	# ensuring the list is reverse ordered
	if remove[i] <= remove[i + 1]:
		print 'i'
# remove triplicates: [13006, 6758, 642], [8022, 2000, 48]
profs.pop(13006)
profs.pop(8022)
profs.pop(6758)
profs.pop(2000)		# these pops require us to redo the duplicate check
# dups = [[18087, 2016], [18085, 8743], [18075, 13871], [16387, 15351], [15709, 15655], [15706, 6747], [15700, 8733], [15677, 14085], [15674, 6092], [15666, 6781], [15637, 13900], [15636, 633], [15627, 6717], [15226, 624], [15225, 10329], [14340, 665], [14336, 634], [14082, 607], [14070, 2034], [14003, 646], [13937, 605], [13919, 8735], [13867, 4684], [13771, 10553], [13003, 4727], [12994, 10935], [12976, 6662], [12672, 10531], [12169, 3334], [12099, 12098], [12050, 12049], [11703, 11702], [11010, 6265], [10940, 7359], [10913, 10911], [10912, 10910], [10879, 4019], [10848, 10532], [10838, 4430], [10810, 10338], [10544, 6736], [10150, 6767], [9970, 4715], [9714, 637], [9610, 1969], [8754, 2022], [8018, 6729], [7377, 2028], [7364, 4711], [7358, 6735], [6760, 617], [5157, 5129], [5156, 5128], [5155, 5127], [5154, 5126], [5153, 5125], [5152, 5124], [5151, 5123], [5150, 5122], [5149, 5121], [5148, 5120], [5147, 5119], [5146, 5118], [5145, 5117], [5144, 5116], [5143, 5115], [5142, 5114], [5141, 5113], [5140, 5112], [5139, 5111], [5138, 5110], [5137, 5109], [5136, 5108], [5135, 5107], [5134, 5106], [5133, 5105], [5132, 5104], [5131, 5103], [5130, 5102], [3920, 1991], [2018, 651]]
for rem in remove:
	profs.pop(rem)
# write to profiles.json, len (should be 19350), old is called profiles_dups

# found bug in getting interests, old file is called profiles_no_ints
profs2 = json.loads(open('profiles_no_ints.json','r').read())
#profs = profs2	# Mar 11, 4pm with Eyal, error at 295, #296 bad profile id
#profs = profs2[297:]	# continue with Eyal, end at 702
#profs = profs2[703:]	# Mar 11, 4pm with Kevin, end at 706 = 1409
#profs = profs2[1410:]	# Mar 11, 4pm with mine, error at 514 = 1924
#profs = profs2[1926:]	# continue with mine, end at 433 = 2359
#profs = profs2[2360:]	# Mar 11, 5pm with Elisha, end at 1003 = 3363
#profs = profs2[3364:]	# Mar 11, 5pm with Karthik, error at 842 = 4206
#profs = profs2[4207:]	# continue with Karthik, end at 160 = 4367
#profs = profs2[4367:]	# Mar 11, 6pm with Tam, end at 1003 = 5370
#profs = profs2[5371:]	# Mar 11, 10pm with Kevin, error at 347 = 5718
#profs = profs2[5720:]	# continue with Kevin, end at 651 = 6371
#profs = profs2[6372:]	# Mar 11, 11pm with Elisha, error at 969 = 7341
#profs = profs2[7342:]	# continue with Elisha, end at 30 = 7372
#profs = profs2[7373:]	# Mar 11, 11pm with Karthik, end at 1004 = 8377
#profs = profs2[8378:]	# Mar 11, 11pm with Tam, end at 1003 = 9381
#profs = profs2[9382:]	# Mar 11, 11pm with Dan, end at 1002 = 10384
#profs = profs2[10385:]	# Mar 12, 12pm with Eyal, error at 687 = 11072
#profs = profs2[11074:]	# continue with Eyal, end at 312 = 11386
#profs = profs2[11387:]	# Mar 12, 1pm with mine, error at 617 = 12004
#profs = profs2[12005:]	# continue with mine, end at 377 = 12382
#profs = profs2[12383:]	# Mar 12, 5pm with Dawei, end at 1002 = 13385
#profs = profs2[13386:]	# Mar 12, 8pm with Dawei, error at 0 = 13386
#profs = profs2[13387:]	# continue with Dawei, error at 254 = 13641
#profs = profs2[13642:]	# continue with Dawei, end at 12 = 13654
#profs = profs2[13655:]	# Mar 12, 8pm with Eyal, end at 1002 = 14657
#profs = profs2[14658:]	# Mar 12, 9pm with Tam, end at 1004 = 15662
#profs = profs2[15663:]	# Mar 12, 9pm with mine, end at 1003 = 16666
#profs = profs2[16667:]	# Mar 13, 11pm with Dawei, end at 2500 = 19167
#profs = profs2[19168:]	# Mar 13, 11pm with mine, end at 181 = 19349
for i in range(len(profs)):
	temp = h.JSONifyProfile(api.get_interests(profs[i]['id']))
	profs[i]['interests'] = temp['interests']
	h.saveProfile(profs[i])
	print i
# save to profiles.json, old is called profiles_dl_ints, size is 19449
for prof in profs:
	h.saveProfile(prof)


# finding number of people on linkedin from a company
search = api.profile_search('keywords=google&count=1&current-company=true')