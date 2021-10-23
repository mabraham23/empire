import sys
import os
import pickle
import copy

sys.path.append(".")

from actions import Action, DistMove, Move, Distribute, Threshold, Designate, Build, Capital
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

  
  def avail_setter(sector):
    avail = sector["avail"]
    avail = avail / (2 * 100)
    if sector["newdes"] != sector["des"]:
      build = 4 * avail / 100
      if build < sector["effic"]:
        sector["effic"] -= build
      else:
        build = sector["effic"]
        sector["effic"] = 0
        sector["des"] = sector["newdes"]
      avail -= build / 4 * 100
    if sector["newdes"] == sector["des"]:
      delta = avail / 100
      build = min(delta, 100 - sector["effic"])
      sector["effic"] += build
      avail -= build * 100

    sector["avail"] = (sector["avail"] / 2 + avail / 100)


  def get_dist_center_of_sector(self, sector):
    x = sector['xdist']
    y = sector['ydist']
    dist_sect = "(" + str(x) + ", " + str(y) + ")"
    return dist_sect


  def update_new_sectors(self, model):
    for key in model['sectors']:
      if ( model['sectors'][key]['newdes'] != model['sectors'][key]['des'] ):
        # print(model['sectors'][key]['newdes'])
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
            if surplus > 0:
              m = DistMove(t_item, key, surplus, dist_sect)
              m.run(model)

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
            if difference > 0:
              m = DistMove(t_item, dist_sect, difference, key)
              m.run(model)

  def sector_effic(self, model):
    pass

  def harvest_natural_reso(self, model):
    if model['sectors']['effic'] > 60:
      for key in model['sectors']:
        product_effic = model['sectors'][key]['effic'] / 100
        if model['sectors'][key]['des'] == 'm':
          product_effic *= (model['sectors'][key]['min'] / 100)
          worker_limit = (model['sectors'][key]['avail'] * product_effic) 
          material_consume = min(worker_limit, model['sectors'][key]['avail'])
          output = material_consume * product_effic
          model['sectors'][key]['iron'] += output
          model['sectors'][key]['avail'] -= round(material_consume/product_effic)

        

  def produce_manufactured_goods(self, model):
    for key in model['sectors']:
      #food
      if model["sectors"][key]["des"] == 15:
        food = model["sectors"][key]["food"]
        food += 100
        model["sectors"][key]["food"] = food
      #mines
      if model["sectors"][key]["des"] == 10:
        iron = model["sectors"][key]["iron"]
        iron += 300
        model["sectors"][key]["iron"] = int(iron)
      # lcm
      if model["sectors"][key]["des"] == 17:
        iron = model["sectors"][key]["iron"]
        lcm = iron * 0.4
        model["sectors"][key]["lcm"] = int(lcm)
        model["sectors"][key]["iron"] = 0
      # hcm
      if model["sectors"][key]["des"] == 18:
        iron = model["sectors"][key]["iron"]
        hcm = iron * 0.3
        model["sectors"][key]["hcm"] = int(hcm)
        model["sectors"][key]["iron"] = 0
        


  def ship_effic(self, model):
    pass

  def food_consumption(self, model):
    pass

  def population_growth(self, model):
    growth_rate = 2
    for key in model["sectors"]:
      civils = model["sectors"][key]["civil"]
      civils += civils * growth_rate
      if civils > 1000:
        civils = 1000
      model["sectors"][key]["civil"] = civils


  def refil_mobility(self, model):
    for key in model['sectors']:
      model["sectors"][key]["mobil"] = 127
      
  def run(self, model):
    #prepare stage
    self.update_new_sectors(model)
    self.set_avail(model)

    #production stage
    # self.update_efficiency()

    self.produce_manufactured_goods(model)
    # distribute items from outside sectors to distribution center
    self.send_to_distribution(model)
    # distribute item from distribution center to outside sectors
    self.distribute_to_sectors(model)
    self.refil_mobility(model)
    self.population_growth(model)
        


def print_sector(model, sect):
  print()
  print(sect)
  print(model['sectors'][sect])
  print()

def print_country(model):
  print()
  print(model['country'])
  print()
