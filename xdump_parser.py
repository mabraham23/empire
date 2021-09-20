#!/usr/bin/env python3

import sys
import os
import pickle

if os.path.exists("sectors.p"):
	fin = open("sectors.p", "rb")
	sectors = pickle.load(fin)
	fin.close()

if os.path.exists("sector-info.p"):
	fin = open("sector-info.p", "rb")
	sectorinfo = pickle.load(fin)
	fin.close()

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
			key = words[0]
			sectorinfo[key] = 0
		elif doc_type == "sect":
			i = -1
			for key in sectorinfo:
				i += 1
				if ( i >= 69 ):
					i = 69
				sectorinfo[key] = words[i]
			x = int(words[1])
			y = int(words[2])
			key = (x,y)
			sectors[key] = sectorinfo
				
for key in sectors:
	print()
	print()
	print(key,":")
	for key2 in sectors[key]:
		print(key2,":",sectors[key][key2])	
	print()
	print()

fout = open("sector-info.p", "wb")
pickle.dump(sectorinfo, fout)
fout.close()

fout = open("sectors.p", "wb")
pickle.dump(sectors, fout)
fout.close()
