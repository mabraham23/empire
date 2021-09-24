#!/usr/bin/env python3

import sys
import os
import pickle
import copy

if os.path.exists("sectors.p"):
	fin = open("sectors.p", "rb")
	sectors = pickle.load(fin)
	fin.close()

if os.path.exists("sector-info.p"):
	fin = open("sector-info.p", "rb")
	sectorinfo = pickle.load(fin)
	fin.close()

	# sectorinfo = {}
	# for key in sectorinfo:
	# 	new = copy.deepcopy(badsectorinfo[key])
	# 	sectorinfo[key] = new

else:
	sectors = {}
	sectorinfo = {}

for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if len(words) > 1:
		if words[1] == "meta":
			doc_type = "meta"	
			continue
		elif words[1] == "sect":
			doc_type = "sect"	
			continue
		if doc_type == "meta":
			key = words[0].replace('"','')
			sectorinfo[key] = ""
		elif doc_type == "sect":
			i = -1
			new_sector_info = {}
			for key in sectorinfo:
				new = copy.deepcopy(sectorinfo[key])
				new_sector_info[key] = new
			for key in new_sector_info:
				i += 1
				if ( i >= 69 ):
					i = 69
				new_sector_info[key] = int(words[i])
			x = int(words[1])
			y = int(words[2])
			tup = str((x,y))	
			key = tup
			sectors[key] = new_sector_info 

if doc_type == "sect":				
	print(sectors)
	# for key in sectors:
	# 	print()
	# 	print()
	# 	print(key,":")
	# 	for key2 in sectors[key]:
	# 		print(key2,":",sectors[key][key2])	
	# 	print()
	# 	print()

elif doc_type == "meta":				
	print(sectorinfo)
	# for key in sectorinfo:
	# 	print()
	# 	print()
	# 	print(key,":")
	# 	print()
	# 	print()

fout = open("sector-info.p", "wb")
pickle.dump(sectorinfo, fout)
fout.close()

fout = open("sectors.p", "wb")
pickle.dump(sectors, fout)
fout.close()
