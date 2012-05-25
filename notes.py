

julia = api.get_profile(member_id = '44KQuE81pC')
j = h.JSONifyProfile(julia)
mit = api.get_company('1503')
m = h.JSONifyCompany(mit)



julia = api.get_profile()
julia.first_name
julia.last_name
julia.headline
julia.public_url


api.get_profile(fields=['id'])
api.get_profile(member_id = 'eDqo5U6S0p', fields=['educations'])
api.get_profile(member_id = '44KQuE81pC', fields=['skills'])

eyal_id = 'eDqo5U6S0p'
julia_id = '44KQuE81pC'
OON_id = 'xwAw1s9fJ5'
OUT_OF_NETWORK:Hhmg
julia1 = api.get_profile(url = str(julia.public_url))


/v1/people/id=44KQuE81pC

api.get_search({'company-name': 'schneider electric', 'count':3})