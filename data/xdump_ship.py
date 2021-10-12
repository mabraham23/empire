#!/usr/bin/env python3

import sys
import os
import pickle
import copy

if os.path.exists("data/ship.p"):
	fin = open("data/ship.p", "rb")
	ship = pickle.load(fin)
	fin.close()
else:
	ship = {}

if os.path.exists("data/ship-info.p"):
	fin = open("data/ship-info.p", "rb")
	shipinfo = pickle.load(fin)
	fin.close()
else:
	shipinfo = {}

doc_type = ""
for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if len(words) > 1:
		if words[1] == "meta":
			doc_type = "meta-sect"	
			continue
		elif words[1] == "ship":
			if shipinfo == {}:
				print("ship info must be present before sectors can be populated")
				break
			doc_type = "ship"	
			continue
		if doc_type == "meta-sect":
			key = words[0].replace('"','')
			shipinfo[key] = ""
		elif doc_type == "ship":
			copy_ship_info = copy.deepcopy(shipinfo)
			for key, word in zip(copy_ship_info, words):
				copy_ship_info[key] = int(word)
			uid = int(words[0])
			ship[uid] = copy_ship_info 

if doc_type == "ship":				
	for key in ship:
		print()
		print(key)
		print(ship[key])
		print()

	fout = open("data/ship.p", "wb")
	pickle.dump(ship, fout)
	fout.close()

elif doc_type == "meta-sect":				
	print(shipinfo)
	fout = open("data/ship-info.p", "wb")
	pickle.dump(shipinfo, fout)
	fout.close()

