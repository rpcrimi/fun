from pytrends.pyGTrends import pyGTrends
import time
import os
import us
from os.path import isfile, join
from pprint import pprint
from random import randint
from csv import DictReader


google_username = "rpcrimi@gmail.com"
google_password = "rpcr!m!1216"
path = "country/"

'''
connector = pyGTrends(google_username, google_password)

states = us.states.mapping('abbr', 'name')
for state in states:
	if state not in ["DK", "OL", "PI", "PR", "GU", "AS", "MP"]:
		connector.request_report("country music", geo="US-%s"%state)
		connector.save_csv(path, "country_music_%s"%state)
'''

country = []
files = ["country/%s"%f for f in os.listdir("country/") if isfile(join("country/", f))]
for file in files:
	with open(file) as csvfile:
		data = list(DictReader(csvfile))

	interests = data[4:648]
	for week in interests:
		if week["Web Search interest: country music"] not in country.keys():
			country.append({"Week": week["Web Search interest: country music"]})

			break
		print country
	break