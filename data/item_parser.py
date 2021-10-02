#!/usr/bin/env python3

import sys
import os
import pickle

items = []

for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if ( len(words) > 5 ):
		items.append({"name": words[1].replace('"', ''), "symbol": words[2].replace('"',''), "weight": int(words[5])})
	else:
		continue

print(items)

fout = open("items.p", "wb")
pickle.dump(items, fout)
fout.close()
