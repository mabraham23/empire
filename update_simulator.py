import sys
import os
import pickle
import copy

sys.path.append(".")

from actions import Action, Move, Distribute, Threshold, Designate, Build, Capital
from model import *

item_thresh_names = ['c_dist','m_dist','s_dist','g_dist','p_dist','i_dist','d_dist','b_dist','f_dist','o_dist','l_dist','h_dist','u_dist','r_dist']
thresh_name_to_item = {'c_dist': 'civil','m_dist': 'milit','s_dist': 'shell','g_dist':'gun','p_dist':'petrol','i_dist':'iron','d_dist':'dust','b_dist': 'bar','f_dist':'food','o_dist':'oil','l_dist':'lcm','h_dist':'hcm','u_dist': 'uw','r_dist': 'rad'}
item_to_thresh_name = {'civil': 'c_dist','milit': 'm_dist','shell': 's_dist','gun':'g_dist','petrol':'p_dist','iron':'i_dist','dust':'d_dist','bar': 'b_dist','food':'f_dist','oil':'o_dist','lcm':'l_dist','hcm':'h_dist','uw': 'u_dist','rad': 'r_dist'}

class Update():

  def __init__(self):
    pass

  def getItemFromDes(self, sect):
    des = self.sectors[sect]['des']
    if des == "j":
      des = "l"
    if des == "k":
      des = "h"
    a = Action()
    print(a.items_dict[15])
    sym = a.items_dict[des]
    dist = sym['symbol'] + "_dist"
    item = self.dist_dict[dist]
    return item

  def show(self, model):
    print()
    print(model['country'])
    print()
    for key in model['sectors']:
      print()
      print(key, ":")
      print(model['sectors'][key])
      print()
  
  def calculate_avail(self, civ, sctwork, milit, uw):
    etu = 60
    avail = round((civ * sctwork / 100.0 + milit / 2.5 + uw) * etu / 100.0)
    return avail

  def get_dist_center_of_sector(self, sector):
    x = sector['xdist']
    y = sector['ydist']
    dist_sect = "(" + str(x) + ", " + str(y) + ")"
    return dist_sect


  def update_new_sectors(self, model):
    for key in model['sectors']:
      if ( model['sectors'][key]['newdes'] != model['sectors'][key]['des'] ):
        model['sectors'][key]['des'] = model['sectors'][key]['newdes']

  def set_avail(self, model):
    for key in model['sectors']:
      model['sectors'][key]['avail'] = self.calculate_avail(model['sectors'][key]['civil'], model['sectors'][key]['work'], model['sectors'][key]['milit'], model['sectors'][key]['uw'])


  def send_to_distribution(self, model):
    for key in model['sectors']:
      for item in item_thresh_names:
        item_thresh = model['sectors'][key][item]
        if item_thresh > 0:
          t_item = thresh_name_to_item[item]
          sect_item_amount = model['sectors'][key][t_item]
          if sect_item_amount > item_thresh:
            # add new items to distribution center 
            dist_sect = self.get_dist_center_of_sector(model['sectors'][key])
            surplus = sect_item_amount - item_thresh
            m = Move(t_item, key, surplus, dist_sect)
            m.dist_move(model)

  def distribute_to_sectors(self, model):
    for key in model['sectors']:
      for item in item_thresh_names:
        item_thresh = model['sectors'][key][item]
        if item_thresh > 0:
          t_item = thresh_name_to_item[item]
          sect_item_amount = model['sectors'][key][t_item]
          if sect_item_amount < item_thresh:
            dist_sect = self.get_dist_center_of_sector(model['sectors'][key])
            difference = item_thresh - sect_item_amount
            m = Move(t_item, dist_sect, difference, key)
            m.dist_move(model)

  def sector_effic(self, model):
    pass

  def harvest_natural_reso(self, model):
    pass

  def produce_manufactured_goods(self, model):
    pass

  def ship_effic(self, model):
    pass

  def food_consumption(self, model):
    pass

  def population_growth(self, model):
    pass

      
  def update(self, model):
    #prepare stage
    # do_feed()
    #avail set
    #production stage
    # produce_sect()
    # effic updated
    # change new_des to des
    self.update_new_sectors(model)
    # calculate and set avail for each sector
    self.set_avail(model)
    # distribute items from outside sectors to distribution center
    self.send_to_distribution(model)
    # distribute item from distribution center to outside sectors
    self.distribute_to_sectors(model)
        


def print_sector(model, sect):
  print()
  print(sect)
  print(model['sectors'][sect])
  print()

def print_country(model):
  print()
  print(model['country'])
  print()

def runCommands():
  model = createModel()
  M = Move('food', '(2, 0)', 300, '(0, 0)')
  M.move(model)


  u = Update()
  u.update(model)
  # print_sector(model, '(-1, -3)')
  # print_sector(model, '(0, 2)')
  # M = Move('food', '(-1, -3)', 100, '(0, 2)')
  # M.dist_move(model)
  # print_country(model)
  # B = Build('ship', '(1, -1)', 'fishing', 1)
  # B.build(model)
  # print_country(model)
  # t = Threshold('dust', '(-1, -3)', 500)
  # t.threshold(model)
  # print_sector(model, '(-1, -3)')
  # print_sector(model, '(0, 2)')
  # d = Designate('(1, 1)', 'h')
  # d.designate(model)
  # u = Update()
  # u.update(model)
  # print_sector(model, '(-1, -3)')
  # d = Distribute('(-1, -3)', '(1, 1)')
  # d.distribute(model)
  # print_sector(model, '(-1, -3)')
  # a = Action()
  # print_sector(model, '(-1, -3)')
  # d = Designate('(-1, -3)', 'c')
  # d.designate(model)
  # print_sector(model, '(-1, -3)')
  # u = Update()
  # u.update(model)
  # print_sector(model, '(-1, -3)')
  # print_country(model)
  # c = Capital('(-1, -3)')
  # c.capital(model)
  # print_country(model)


# need to update mobility cost when distributing
# need to find where ship is shown



runCommands()