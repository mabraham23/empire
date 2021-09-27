#!/usr/bin/env python3

import sys
import os
import pickle

des = {}

for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if ( len(words) > 15 ):
		des[int(words[0])] = {"name": words[1].replace('"', ''), "symbol": words[2].replace('"','')}
	else:
		continue

print(des)

fout = open("designations.p", "wb")
pickle.dump(des, fout)
fout.close()
