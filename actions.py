#!/usr/bin/env python3

import sys
import os
import pickle

if os.path.exists("sectors.p"):
	fin = open("sectors.p", "rb")
	sectors = pickle.load(fin)
	fin.close()

print("start:", sectors[(0,0)]['"food"'])


class Move():

	def __init__(self,item,source,number,dest):
		self.item = item
		self.source = source
		self.number = number
		self.dest = dest

	def move(self):
		sector_copy = sectors
		curr = sector_copy[self.source][self.item]
		new = int(curr) - self.number
		sector_copy[self.source][self.item] = new
			
		curr1 = sector_copy[self.dest][self.item]
		new = int(curr1) + self.number
		sector_copy[self.dest][self.item] = new

		for key in sector_copy:
			print()
			print(key,":")
			for key2 in sector_copy[key]:
				print(key2,":",sector_copy[key][key2])	
			print()
		
		fout = open("sectors.p", "wb")
		pickle.dump(sector_copy, fout)
		fout.close()

#	def distribute(self,source,dest):

#	def threshold(self,item,sect,thresh):

#	def designate(self,sect,des):

#	def build(self,kind,sect,v_type,quantity):

#	def capital(self,sect):

def do_stuff():
	a = Move('"food"',(0,0),10,(0,2))
	a.move()

do_stuff()
