#!/usr/bin/env python3

import sys
import os
import pickle
import copy

if os.path.exists("data/country.p"):
	fin = open("data/country.p", "rb")
	country = pickle.load(fin)
	fin.close()
else:
  country = {}

if os.path.exists("data/country-info.p"):
	fin = open("data/country-info.p", "rb")
	countryinfo= pickle.load(fin)
	fin.close()
else:
  countryinfo = {}

for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if len(words) > 1:
		if words[1] == "meta":
			doc_type = "meta"
			continue
		elif words[1] == "country":
			doc_type = "country"	
			continue
		if doc_type == "meta":
			key = words[0].replace('"','')
			countryinfo[key] = ""
		elif doc_type == "country":
			new_country_info = {}
			for key in countryinfo:
				new = copy.deepcopy(countryinfo[key])
				new_country_info[key] = new
			i = -1
			for key in new_country_info:
				i += 1
				if ( i >= 22 ):
					i = 22
				if ( i == 2 or i == 3):
					country[key] = str(words[i].replace('"',''))
				elif ( i == 21 or i == 20 or i == 19 or i == 18):
					country[key] = float(words[i])
				else:
					country[key] = int(words[i])


if doc_type == "country":				
	print(country)

elif doc_type == "meta":				
	print(countryinfo)

fout = open("data/country-info.p", "wb")
pickle.dump(countryinfo, fout)
fout.close()

fout = open("data/country.p", "wb")
pickle.dump(country, fout)
fout.close()
