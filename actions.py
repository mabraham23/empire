#!/usr/bin/env python3

import sys
import os
import pickle
import copy

if os.path.exists("sectors.p"):
	fin = open("sectors.p", "rb")
	bad_sectors = pickle.load(fin)
	fin.close()

	sectors = {}
	for key in bad_sectors:
		new = copy.deepcopy(bad_sectors[key])
		sectors[key] = new

if os.path.exists("designations.p"):
	fin = open("designations.p", "rb")
	des_dict = pickle.load(fin)
	fin.close()

class Action():
	def __init__(self):
		pass

	def show(self):
		print()
		for key in sectors:
			print()
			print(key, ":")
			print(sectors[key])
			print()

	def show_sect(self, sect):
		print()
		print(sect)
		print()
		for key in sectors[sect]:
			print(key, ":", sectors[sect][key])
		print()
			
	def save(self):
		fout = open("sectors.p", "wb")
		pickle.dump(sectors, fout)
		fout.close()
		

class Move(Action):

	def __init__(self,item,source,number,dest):
		self.item = item
		self.source = source
		self.number = number
		self.dest = dest

	def move(self):
		curr = sectors[self.source][self.item]
		new = curr - self.number
		if ( new < 0 ):
			print("\nCannot move more", self.item, "than you have available. Only", curr, self.item, "remain in sector", self.source, "\n")
		else:
			sectors[self.source][self.item] = new
			curr = sectors[self.dest][self.item]
			new = curr + self.number
			if ( new > 9999 ):
				new = 9999
				print("limit has been reached for", self.item, "in sector", self.dest + ".", "limit is", new)
			sectors[self.dest][self.item] = new
		

#	def distribute(self,source,dest):

#	def threshold(self,item,sect,thresh):

class Designate(Action):

	def __init__(self,sect,des):
		self.sect = sect
		self.des = des 

	def designate(self):
		if self.des in des_dict:
			print(des_dict[self.des])
			sectors[self.sect]['des'] = des_dict[self.des]
		else:
			print("invalid designation given", self.des)	


#	def build(self,kind,sect,v_type,quantity):

class Capital(Action):

	def __init__(self,sect):
		self.sect = sect

	def capital(self):
		key_list = list(des_dict.keys())
		val_list = list(des_dict.values()) 
		if sectors[self.sect]['des'] in [1, 5]:
			print("capital des", des_dict['c'])
			sectors[sect]['des'] = des_dict['c']
		else:
			print("the sector must have a designation of type 'c' (capital) or '^' (mountain) to be a capital. Sector of type", "'" + key_list[val_list.index(sectors[self.sect]['des'])] + "' given.")


def do_stuff():
	# a = Move('food','(0, 0)',100,'(0, 2)')
	# a.move()
	# d = Designate('(0, 0)', 'a')
	# d.designate()
	c = Capital('(0, 2)')
	c.show()
	# c.capital()
	

do_stuff()
