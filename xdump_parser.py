#!/usr/bin/env python3

import sys

print("hopefully this did something")

sectors = {}
for line in sys.stdin.readlines():
	line = line.strip()
	words = line.split()
	if len(words) < 10:
		continue
	x = int(words[1])
	y = int(words[2])
	key = (x,y)
	sectors[key] = words
