#!/usr/bin/env python3

import sys
import os
import pickle

des = {}

for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if ( len(words) > 15 ):
		des[words[2].replace('"', '')] = int(words[0])
	else:
		continue

print(des)

fout = open("designations.p", "wb")
pickle.dump(des, fout)
fout.close()
