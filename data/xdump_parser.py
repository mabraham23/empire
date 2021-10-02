#!/usr/bin/env python3

import sys
import os
import pickle
import copy

if os.path.exists("sectors.p"):
	fin = open("sectors.p", "rb")
	sectors = pickle.load(fin)
	fin.close()
else:
	sectors = {}

if os.path.exists("sector-info.p"):
	fin = open("sector-info.p", "rb")
	sectorinfo = pickle.load(fin)
	fin.close()
else:
	sectorinfo = {}

doc_type = ""
for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if len(words) > 1:
		if words[1] == "meta":
			doc_type = "meta-sect"	
			continue
		elif words[1] == "sect":
			if sectorinfo == {}:
				print("sector info must be present before sectors can be populated")
				break
			doc_type = "sect"	
			continue
		if doc_type == "meta-sect":
			key = words[0].replace('"','')
			sectorinfo[key] = ""
		elif doc_type == "sect":
			copy_sector_info = copy.deepcopy(sectorinfo)
			for key, word in zip(copy_sector_info, words):
				copy_sector_info[key] = int(word)
			x = int(words[1])
			y = int(words[2])
			xy_key = str((x,y))	
			sectors[xy_key] = copy_sector_info

if doc_type == "sect":				
	for key in sectors:
		print()
		print(key)
		print(sectors[key])
		print()

	fout = open("sectors.p", "wb")
	pickle.dump(sectors, fout)
	fout.close()

elif doc_type == "meta-sect":				
	print(sectorinfo)

	fout = open("sector-info.p", "wb")
	pickle.dump(sectorinfo, fout)
	fout.close()

