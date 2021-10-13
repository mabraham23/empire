#!/usr/bin/env python3

import sys
import os
import pickle
import copy
import math

if os.path.exists("data/designations.p"):
  fin = open("data/designations.p", "rb")
  des_dict = pickle.load(fin)
  fin.close()

if os.path.exists("data/items.p"):
  fin = open("data/items.p", "rb")
  items_list = pickle.load(fin)
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

dist_item_dict = {'civil': 'c_dist','milit': 'm_dist','shell': 's_dist','gun':'g_dist','petrol':'p_dist','iron':'i_dist','dust':'d_dist','bar': 'b_dist','food':'f_dist','oil':'o_dist','lcm':'l_dist','hcm':'h_dist','uw': 'u_dist','rad': 'r_dist'}
dist_dict = {'c_dist': 'civil','m_dist': 'milit','s_dist': 'shell','g_dist':'gun','p_dist':'petrol','i_dist':'iron','d_dist':'dust','b_dist': 'bar','f_dist':'food','o_dist':'oil','l_dist':'lcm','h_dist':'hcm','u_dist': 'uw','r_dist': 'rad'}

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

  def getWeight(self, item):
    if item in weight_dict:
      return weight_dict[item]		
    else:
      return weight_dict['other']		

  def printActions(self, actions):
    print(actions)

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

  def calculatePathCost(self, sectors, source, dest):
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
  
  def get_items_list(self):
    items = []
    for key in dist_dict:
      items.append(dist_dict[key])
    return items

  def show_items(self):
    print()
    print(items_list)
    print()

  def print_sector(self, model, sect):
    print()
    print(sect)
    print(model['sectors'][sect])
    print()
  
  def get_sector_list(self, model):
    sectors = []
    for key in model['sectors']:
      sectors.append(key)
    return sectors

  def get_des_name_for_sect(self, model, sect):
    num_des = model['sectors'][sect]['des']
    sym_des = des_dict[num_des]['name']
    return sym_des

  def get_des_sym_for_sect(self, model, sect):
    num_des = model['sectors'][sect]['des']
    sym_des = des_dict[num_des]['sym']
    return sym_des



class DistMove(Action):
  def __init__(self,item,source,number,dest):
    super().__init__()
    self.item = item
    self.source = source
    self.number = number
    self.dest = dest

  def run(self, model):
    curr = model['sectors'][self.source][self.item]
    mcost = (self.calculatePathCost(model['sectors'], self.source, self.dest) / 10 * self.getWeight(self.item) / 10)
    # print("mcost", mcost)
    mob_sect = model['sectors'][self.source]['mobil']
    if mcost > mob_sect:
      print("Cannot do distribute move. Not enough mobility. Mobility Cost:", mcost, "Mobility for sector", self.source + ": ", mob_sect)
      return -1
    new_mob = round(mob_sect - mcost)
    new_amount = curr - self.number
    if ( new_amount < 0 ):
      return
      # print("\nCannot move more", self.item, "than you have available. Only", curr, self.item, "are available in sector", self.source, "\n")
      # return -1
    else:
      model['sectors'][self.source][self.item] = new_amount
      model['sectors'][self.source]['mobil'] = new_mob
      # print("number of", self.item, "before distribution from sector", self.source, "is", curr)
      # print("number of", self.item, "remaining in source sector", self.source, "after distribution", new_amount)
      # print()
      # print("number of mob before distribution from source sector", self.source, "is", mob_sect)
      # print("number of mob remaining in source sector", self.source, "after distribution", new_mob)
      # print()
      dest_curr = model['sectors'][self.dest][self.item]
      new_amount = dest_curr + self.number
      # print()
      # print("number of", self.item, "in dest sect", self.dest, "before distribution was", dest_curr)
      # print("number of", self.item, "in dest sect", self.dest, "after distribution is", new_amount)
      if ( new_amount > 9999 ):
        new_amount = 9999
        print("limit has been reached for", self.item, "in sector", self.dest + ".", "truncated at", new_amount)
      model['sectors'][self.dest][self.item] = new_amount


class Move(Action):

  def __init__(self,item=0,source=0,number=0,dest=0):
    super().__init__()
    self.item = item
    self.source = source
    self.number = number
    self.dest = dest

  def calc_mobility(self, model):
    bonus = self.getBonus(model['sectors'][self.source]['des'], self.item)
    mob_cost = int((self.number) * (self.getWeight(self.item)) * (self.calculatePathCost(model['sectors'], self.source, self.dest)) / bonus)
    return mob_cost

  def calc_param_mobil(self, model, source, dest, amount, item):
    bonus = self.getBonus(model['sectors'][source]['des'], item)
    mob_cost = int((amount) * (self.getWeight(item)) * (self.calculatePathCost(model['sectors'], source, dest)) / bonus)
    return mob_cost

  def calc_max_move(self, model, source, dest, item ):
    max_mobil = 0
    amount = 1
    while max_mobil <= model['sectors'][source]["mobil"]:
      max_mobil = self.calc_param_mobil(model, source, dest, amount, item)
      amount += 1
    return (amount -2), max_mobil

  def calc_max_move_list(self, model, source, dest_list, item , goal):
    max_mobil = model['sectors'][source]["mobil"] 
    move_amounts = []
    total_diff = 0
    for dest in dest_list:
      curr = model["sectors"][dest][item]
      diff = goal - curr
      total_diff += diff
    for dest in dest_list:
      model["sectors"][dest][item]
      curr = model["sectors"][dest][item]
      diff = goal - curr
      dest_goal_perc = diff / total_diff
      allocated_mob = math.floor(dest_goal_perc * max_mobil)
      amount = 1
      sect_mobil = 0
      while sect_mobil <= allocated_mob and (amount + curr) != goal:
        sect_mobil = self.calc_param_mobil(model, source, dest, amount, item)
        amount += 1
      move_item = {} 
      move_item["dest"] = dest
      move_item["amount"] = amount - 2
      move_amounts.append(move_item)
    return move_amounts

  def run(self, model):
    curr = model['sectors'][self.source][self.item]
    bonus = self.getBonus(model['sectors'][self.source]['des'], self.item)
    mob_cost = int((self.number) * (self.getWeight(self.item)) * (self.calculatePathCost(model['sectors'], self.source, self.dest)) / bonus)
    mob_sect = model['sectors'][self.source]['mobil']
    if mob_cost > mob_sect:
      print("Cannot do move. Not enough mobility. Mobility Cost:", mob_cost, "Mobility for sector", self.source + ": ", mob_sect)
    else:
      new_mob = mob_sect - mob_cost
      new_amount = curr - self.number
      if ( new_amount < 0 ):
        print("\nCannot move more", self.item, "than you have available. Only", curr, self.item, "remain in sector", self.source, "\n")
      else:
        model['sectors'][self.source][self.item] = new_amount
        model['sectors'][self.source]['mobil'] = new_mob
        # print("number of", self.item, "before move from sector", self.source, "is", curr)
        # print("number of", self.item, "remaining in source sector", self.source, "is", new_amount)
        # print()
        # print("number of mob before move from source sector", self.source, "is", mob_sect)
        # print("number of mob remaining in source sector", self.source, "is", new_mob)
        # print()
        dest_curr = model['sectors'][self.dest][self.item]
        new_amount = dest_curr + self.number
        # print("number of", self.item, "in dest sect", self.dest, "before move was", dest_curr)
        # print("number of", self.item, "in dest sect", self.dest, "after move is", new_amount)
        # print()
        if ( new_amount > 9999 ):
          new_amount = 9999
          print("limit has been reached for", self.item, "in sector", self.dest + ".", "truncated at", new_amount)
        model['sectors'][self.dest][self.item] = new_amount
        return("move " + self.item + " " + self.source[1:-1].replace(" ", "") + " " + str(self.number) + " " + self.dest[1:-1].replace(" ", ""))


class Distribute(Action):
  def __init__(self,source,dest):
    super().__init__()
    self.source = source
    self.dest = dest 

  def run(self, model):
    if self.source in model['sectors']:
      if self.dest in model['sectors']:
        if model['sectors'][self.dest]['des'] in [12, 13]:
          x,y = self.coordToInt(self.dest)
          model['sectors'][self.source]['xdist'] = x
          model['sectors'][self.source]['ydist'] = y
          return("distribute " + self.source[1:-1].replace(" ", "") + " " + self.dest[1:-1].replace(" ", ""))
        else:
          print("dest in not a harbor or a warehouse. dest is:", "'" + self.get_des_name_for_sect(model, self.dest) + "'", model['sectors'][self.dest]['des'], " harbor is 12, and warehouse is 13")
      else:
        print("dest given is not a valid sector; sector given:", self.dest, "valid sectors:", self.get_sector_list(model))
    else:
      print("source given is not a valid sector; sector given:", self.source, "valid sectors:", self.get_sector_list(model))


class Threshold(Action):
  def __init__(self,item,sect,thresh):
    super().__init__()
    self.item = item
    self.sect = sect
    self.thresh = thresh

  def run(self, model):
    if self.item in self.get_items_list():
      if self.sect in self.get_sector_list(model):
        if (self.thresh >= 0 and self.thresh < 9999):
          thresh = dist_item_dict[self.item]
          model['sectors'][self.sect][thresh] = int(self.thresh)
          return("threshold " + self.item + " " + self.sect[1:-1].replace(" ", "") + " " + str(self.thresh))
        else:
          print("invalid value for thresh given:", self.thresh, "Value must be positive interger greater than or equal to 0 and less than 9999")
      else:
        print("source given is not a valid sector; sector given:", self.source, "valid sectors:", self.get_sector_list(model))
    else:
      print("invalid item given:", self.item, "valid items are:", self.get_items_list())
    


class Designate(Action):

  def __init__(self,sect,des):
    super().__init__()
    self.sect = sect
    self.des = des 

  def run(self, model):
    if self.des in self.getDesList():
      if model['sectors'][self.sect]['coastal'] == 0 and self.des == 'h':
        print("only coastal sects may be designated as harbors, sector given", self.sect)	
      else:
        if model['sectors'][self.sect]['des'] == 4 or model['sectors'][self.sect]['des'] == 5:
          # print(self.getDesDictSim()[self.des])
          model['sectors'][self.sect]['des'] = self.getDesDictSim()[self.des]
          model['sectors'][self.sect]['newdes'] = self.getDesDictSim()[self.des]
        else:
          model['sectors'][self.sect]['newdes'] = self.getDesDictSim()[self.des]
        return("designate " + self.sect[1:-1].replace(" ", "") + " " + self.des)
    else:
      print("invalid designation given", self.des, "valid designations are:", self.getDesList())	


class Build(Action):

  def __init__(self,kind,sect,v_type,quantity):
    super().__init__()
    self.kind = kind
    self.sect = sect
    self.v_type = v_type
    self.quantity = quantity

  def run(self, model):
    if self.kind in build_types:
      if self.sect in self.get_sector_list(model):
        if model['sectors'][self.sect]['des'] == 12:
          if self.v_type in ship_types:
            if self.quantity > 0 and self.quantity < 10:
              if model['sectors'][self.sect]['lcm'] >= ship_info[self.v_type]['lcm'] * self.quantity:
                if model['sectors'][self.sect]['hcm'] >= ship_info[self.v_type]['hcm'] * self.quantity:
                  if model['sectors'][self.sect]['avail'] >= ship_info[self.v_type]['avail'] * self.quantity:
                    if model['country']['money'] >= ship_info[self.v_type]['cost']:
                      lcm = model['sectors'][self.sect]['lcm'] 
                      hcm = model['sectors'][self.sect]['hcm'] 
                      avail = model['sectors'][self.sect]['avail'] 
                      model['country']['money'] = model['country']['money'] - ship_info[self.v_type]['cost']
                      model['sectors'][self.sect]['lcm'] = lcm - (ship_info[self.v_type]['lcm'] * self.quantity)
                      model['sectors'][self.sect]['hcm'] = hcm - (ship_info[self.v_type]['hcm'] * self.quantity)
                      model['sectors'][self.sect]['avail'] = avail - (ship_info[self.v_type]['avail'] * self.quantity)
                      model['ships']["fishing"] += self.quantity
                      return("build " + self.kind + " " + self.sect[1:-1].replace(" ","") + " " + self.v_type + " " + str(self.quantity))
                    else:
                      print("not enough money. cost of frigate is:", ship_info[self.v_type]['cost'] + ".", "Money in country:", model['country']['money'])
                  else:
                    print("not enough avail in sector", self.sect, "amount:", model['sectors'][self.sect]['avail'], "amount required: ", ship_info[self.v_type]['avail'] * self.quantity)
                else:
                  print("not enough hcm in sector", self.sect, "amount:", model['sectors'][self.sect]['hcm'], "amount required: ", ship_info[self.v_type]['hcm'] * self.quantity)
              else:
                print("not enough lcm in sector", self.sect, "amount:", model['sectors'][self.sect]['lcm'], "amount required: ", ship_info[self.v_type]['lcm'] * self.quantity)
            else:
              print("invalid quantity given", self.quantity, "quantity must be greater than 0 and less than 10")
          else:
            print("invalid ship type given:", self.v_type, "valid ship types are:", self.ship_types)
        else:
          print("sector given is not a harbor. Ships may only be built in a harbor sector. Number 12")
      else:
        print("sector given is not a valid sector; sector given:", self.sect, "valid model['sectors']:", self.get_sector_list(model))
    else:
      print("invalid build type given:", self.kind, "build types are:", self.build_types)	


class Capital(Action):

  def __init__(self,sect):
    self.sect = sect

  def run(self, model):
    if model['sectors'][self.sect]['des'] in [1, 5]:
      coord = self.intsToCoord(model['country']['xcap'], model['country']['ycap'])	
      if self.sect != coord:
        x, y = self.coordToInt(self.sect)
        model['country']['xcap'] = x
        model['country']['ycap'] = y
        return("capital " + self.sect[1:-1].replace(" ", ""))
      else:
        print("the sector", self.sect, "is already a capitol")
    else:
      print("the sector must have a designation of type 'c' (capital) or '^' (mountain) to be a capital. Sector of type" + " '" + des_dict[model['sectors'][self.sect]['des']]['symbol'] + "' " + "given")


