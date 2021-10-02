#!/usr/bin/env python3

import sys
import os
import pickle
import copy

if os.path.exists("data/designations.p"):
  fin = open("data/designations.p", "rb")
  des_dict = pickle.load(fin)
  fin.close()

if os.path.exists("data/items.p"):
  fin = open("data/items.p", "rb")
  items_list = pickle.load(fin)
  fin.close()

if os.path.exists("data/country.p"):
  fin = open("data/country.p", "rb")
  country = pickle.load(fin)
  fin.close()

if os.path.exists("data/sectors.p"):
  fin = open("data/sectors.p", "rb")
  sectors = pickle.load(fin)
  fin.close()

weight_dict = { 'bar': 50, 'gun': 10, 'rad': 8, 'dust': 5, 'uw': 2, 'other': 1, }
build_types = ['ship', 'plane', 'land', 'nuke']
ship_types = ['fishing', 'frigate']
ship_info = {
  'fishing': {'lcm': 25, 'hcm': 15, 'avail': 75, 'cost': 180},
  'frigate': {'lcm': 30, 'hcm': 30, 'avail': 110, 'cost': 600}
}
bonus_dict = { 
  12: {'mil': 1, 'uw': 2, 'civ': 10, 'bar': 5, 'other': 10}, 
  13: {'mil': 1, 'uw': 2, 'civ': 10, 'bar': 5, 'other': 10}, 
  29: {'mil': 1, 'uw': 1, 'civ': 10, 'bar': 4, 'other': 1}, 
  99: {'mil': 1, 'uw': 1, 'civ': 10, 'bar': 1, 'other': 1}
}

class Action():
  def __init__(self):
    self.items_dict = items_list

  def getBonus(self, des_num, item):
    if des_num in des_dict:
      if des_num in bonus_dict:
        if item in bonus_dict[des_num]:
          return bonus_dict[des_num][item]
        else:
          return bonus_dict[des_num]['other']
      else:
        if item in bonus_dict[99]:
          return bonus_dict[99][item]
        else:
          return bonus_dict[99]['other']
    else:
      print('invalid des_num given', des_num)
      return -1

  def getWeight(self, item):
    if item in weight_dict:
      return weight_dict[item]		
    else:
      return weight_dict['other']		

  def getDesList(self):
    dl = []
    for key in des_dict:
      dl.append(des_dict[key]['symbol'])
    return dl

  def getDesDictSim(self):
    dls = {}
    i = 0
    for key in des_dict:
      dls[des_dict[key]['symbol']] = i
      i += 1 
    return dls
  
  def coordToInt(self, coord):
    nc = coord.strip("()")
    sc = nc.split(",")
    x = int(sc[0])
    y = int(sc[1])
    return x,y

  def intsToCoord(self, x, y):
    return "(" + str(x) + ", " + str(y) + ")"

  def calculatePathCost(self, source, dest):
    if source in sectors:
      if dest in sectors:
        s_x, s_y = self.coordToInt(source)
        d_x, d_y = self.coordToInt(dest)
        dist = (abs(d_y - s_y ) + abs(d_x - s_x))//2
        return dist * 0.4
      else:
        print("invalid source given", dest, "valid sectors are", self.getSectorList())
        return -1
    else:
      print("invalid source given", source, "valid sectors are", self.getSectorList())
      return -1
  
  def getSectorList(self):
    sectorList = []	
    for key in sectors:
      sectorList.append(key)
    return sectorList

  def getItemsList(self):
    items = []
    for i in range(len(items_list)):
      items.append(items_list[i]['name'])
    return items

  def show_items(self):
    print()
    print(items_list)
    print()

  def show(self):
    print()
    print(country)
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

    fout = open("country.p", "wb")
    pickle.dump(country, fout)
    fout.close()


class Move(Action):

  def __init__(self,item,source,number,dest):
    super().__init__()
    self.item = item
    self.source = source
    self.number = number
    self.dest = dest

  def dist_move(self):
    curr = sectors[self.source][self.item]
    mcost = (self.calculatePathCost(self.source, self.dest) / 10 * self.getWeight(self.item) / 10)
    print("mcost", mcost)
    mob_sect = sectors[self.source]['mobil']
    if mcost > mob_sect:
      print("Cannot do distribute move. Not enough mobility. Mobility Cost:", mcost, "Mobility for sector", self.source + ": ", mob_sect)
      return -1
    new_mob = round(mob_sect - mcost)
    new_amount = curr - self.number
    if ( new_amount < 0 ):
      print("\nCannot move more", self.item, "than you have available. Only", curr, self.item, "remain in sector", self.source, "\n")
      return -1
    else:
      sectors[self.source][self.item] = new_amount
      sectors[self.source]['mobil'] = new_mob
      print("number of", self.item, "remaining in sector", self.source, "is", new_amount)
      print("number of mob remaining in sector", self.source, "is", new_mob)
      curr = sectors[self.dest][self.item]
      new_amount = curr + self.number
      if ( new_amount > 9999 ):
        new_amount = 9999
        print("limit has been reached for", self.item, "in sector", self.dest + ".", "truncated at", new_amount)
      sectors[self.dest][self.item] = new_amount

  def move(self, model):
    model = model['sectors']
    curr = model[self.source][self.item]
    bonus = self.getBonus(model[self.source]['des'], self.item)
    mob_cost = int((self.number) * (self.getWeight(self.item)) * (self.calculatePathCost(self.source, self.dest)) / bonus)
    mob_sect = model[self.source]['mobil']
    if mob_cost > mob_sect:
      print("Cannot do move. Not enough mobility. Mobility Cost:", mob_cost, "Mobility for sector", self.source + ": ", mob_sect)
      return -1
    new_mob = mob_sect - mob_cost
    new_amount = curr - self.number
    if ( new_amount < 0 ):
      print("\nCannot move more", self.item, "than you have available. Only", curr, self.item, "remain in sector", self.source, "\n")
      return -1
    else:
      model[self.source][self.item] = new_amount
      model[self.source]['mobil'] = new_mob
      print("number of", self.item, "remaining in sector", self.source, "is", new_amount)
      print("number of mob remaining in sector", self.source, "is", new_mob)
      curr = model[self.dest][self.item]
      new_amount = curr + self.number
      if ( new_amount > 9999 ):
        new_amount = 9999
        print("limit has been reached for", self.item, "in sector", self.dest + ".", "truncated at", new_amount)
      model[self.dest][self.item] = new_amount
    

# designate to which sector to send resources
class Distribute(Action):
  def __init__(self,source,dest):
    super().__init__()
    self.source = source
    self.dest = dest 

  def distribute(self):
    if self.source in sectors:
      if self.dest in sectors:
        x,y = self.coordToInt(self.dest)
        sectors[self.source]['xdist'] = x
        sectors[self.source]['ydist'] = y
        print(sectors[self.source])
      else:
        print("dest given is not a valid sector; sector given:", self.dest, "valid sectors:", self.getSectorList())
        return -1
    else:
      print("source given is not a valid sector; sector given:", self.source, "valid sectors:", self.getSectorList())
      return -1


class Threshold(Action):
  def __init__(self,item,sect,thresh):
    super().__init__()
    self.item = item
    self.sect = sect
    self.thresh = thresh

  def threshold(self):
    if self.item in self.getItemsList():
      if self.sect in self.getSectorList():
        if (self.thresh > 0 and self.thresh < 9999):
          sym = self.item[0] + '_dist'
          sectors[self.sect][sym] = int(self.thresh)
        else:
          print("invalid value for thresh given:", self.thresh, "Value must be positive interger greater than 0 and less than 9999")
      else:
        print("source given is not a valid sector; sector given:", self.source, "valid sectors:", self.getSectorList())
    else:
      print("invalid item given:", self.item, "valid items are:", self.getItemsList())
    


class Designate(Action):

  def __init__(self,sect,des):
    super().__init__()
    self.sect = sect
    self.des = des 

  def designate(self):
    if self.des in self.getDesList():
      if sectors[self.sect]['coastal'] == 0 and self.des == 'h':
        print("only coastal sectors may be designated as harbors, sector given", self.sect)	
        return -1 
      else:
        if sectors[self.sect]['effic'] <= 5:
          sectors[self.sect]['effic'] = 0
        sectors[self.sect]['newdes'] = self.getDesDictSim()[self.des]
    else:
      print("invalid designation given", self.des, "valid designations are:", self.getDesList())	
      return -1


class Build(Action):

  def __init__(self,kind,sect,v_type,quantity):
    super().__init__()
    self.kind = kind
    self.sect = sect
    self.v_type = v_type
    self.quantity = quantity

  def build(self):
    if self.kind in self.build_types:
      if self.sect in self.getSectorList():
        if sectors[self.sect]['des'] == 12:
          if self.v_type in self.ship_types:
            if self.quantity > 0 and self.quantity < 10:
              if sectors[self.sect]['lcm'] >= self.ship_info[self.v_type]['lcm'] * self.quantity:
                if sectors[self.sect]['hcm'] >= self.ship_info[self.v_type]['hcm'] * self.quantity:
                  if sectors[self.sect]['avail'] >= self.ship_info[self.v_type]['avail'] * self.quantity:
                    lcm = sectors[self.sect]['lcm'] 
                    hcm = sectors[self.sect]['hcm'] 
                    avail = sectors[self.sect]['avail'] 
                    print(sectors[self.sect])
                    sectors[self.sect]['lcm'] = lcm - (self.ship_info[self.v_type]['lcm'] * self.quantity)
                    sectors[self.sect]['hcm'] = hcm - (self.ship_info[self.v_type]['hcm'] * self.quantity)
                    sectors[self.sect]['avail'] = avail - (self.ship_info[self.v_type]['avail'] * self.quantity)
                    print(sectors[self.sect])
                  else:
                    print("not enough avail in sector", self.sect, "amount:", sectors[self.sect]['avail'], "amount required: ", self.ship_info[self.v_type]['avail'] * self.quantity)
                else:
                  print("not enough hcm in sector", self.sect, "amount:", sectors[self.sect]['hcm'], "amount required: ", self.ship_info[self.v_type]['hcm'] * self.quantity)
              else:
                print("not enough lcm in sector", self.sect, "amount:", sectors[self.sect]['lcm'], "amount required: ", self.ship_info[self.v_type]['lcm'] * self.quantity)
            else:
              print("invalid quantity given", self.quantity, "quantity must be greater than 0 and less than 10")
          else:
            print("invalid ship type given:", self.v_type, "valid ship types are:", self.ship_types)
        else:
          print("sector given is not a harbor. Ships may only be build in a harbor sector. Number 12")
      else:
        print("sector given is not a valid sector; sector given:", self.sect, "valid sectors:", self.getSectorList())
    else:
      print("invalid build type given:", self.kind, "build types are:", self.build_types)	


class Capital(Action):

  def __init__(self,sect):
    self.sect = sect

  def capital(self):
    if sectors[self.sect]['des'] in [1, 5]:
      coord = self.intsToCoord(country['xcap'], country['ycap'])	
      if self.sect != coord:
        x, y = self.coordToInt(self.sect)
        country['xcap'] = x
        country['ycap'] = y
      else:
        print("the sector", self.sect, "is already a capitol")
    else:
      print("the sector must have a designation of type 'c' (capital) or '^' (mountain) to be a capital. Sector of type" + " '" + des_dict[sectors[self.sect]['des']]['symbol'] + "' " + "given")


