import sys
import os
import pickle
import copy
import math

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
  

  



  def get_dist_center_of_sector(self, sector):
    x = sector['xdist']
    y = sector['ydist']
    dist_sect = "(" + str(x) + ", " + str(y) + ")"
    return dist_sect


  # def update_new_sectors(self, model):
  #   for key in model['sectors']:
  #     if ( model['sectors'][key]['newdes'] != model['sectors'][key]['des'] ):
  #       # print(model['sectors'][key]['newdes'])
  #       model['sectors'][key]['des'] = model['sectors'][key]['newdes']


  def calculate_avail(self, civ, sctwork, milit, uw):
    etu = 60
    avail = math.floor((civ * sctwork / 100.0 + milit / 2.5 + uw) * etu / 100.0)
    return avail

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

  def set_effic(self, model):
    for key in model["sectors"]:
      avail = model["sectors"][key]["avail"]
      avail = avail / 2 * 100
      if model["sectors"][key]["newdes"] != model["sectors"][key]["des"]:
        build = 4 * avail / 100
        if build < model["sectors"][key]["effic"]:
          model["sectors"][key]["effic"] -= build
        else:
          build = model["sectors"][key]["effic"]
          model["sectors"][key]["effic"] = 0
          model["sectors"][key]["des"] = model["sectors"][key]["newdes"]
        avail -= build / 4 * 100
      if model["sectors"][key]["newdes"] == model["sectors"][key]["des"]:
        delta = avail / 100
        build = min(delta, 100 - model["sectors"][key]["effic"])
        model["sectors"][key]["effic"] += math.floor(build)
        avail -= build * 100

      model["sectors"][key]["avail"] = model["sectors"][key]["avail"] / 2 + avail / 100

  def harvest_natural_resources(self, model):
    for key in model["sectors"]:
      if model['sectors'][key]['effic'] > 60:
        # mining resources
        if model['sectors'][key]['des'] == 10:
          product_effic = model['sectors'][key]['effic'] / 100
          product_effic *= (model['sectors'][key]['min'] / 100)
          worker_limit = (model['sectors'][key]['avail'] * product_effic) 
          material_consume = worker_limit
          # material_consume = min(worker_limit, model['sectors'][key]['avail'])
          output = material_consume * product_effic

          model['sectors'][key]['iron'] += output
          model['sectors'][key]['avail'] -= math.floor(material_consume/product_effic)
          if (product_effic > 0):
            model['sectors'][key]['avail'] -= math.floor(material_consume/product_effic)

        # harvest agricultrue
        elif model['sectors'][key]['des'] == 15:
          product_effic = model['sectors'][key]['effic'] / 100
          product_effic *= (model['sectors'][key]['fert'] / 100)
          worker_limit = (model['sectors'][key]['avail'] * product_effic) 
          material_consume = worker_limit
          # material_consume = min(worker_limit, model['sectors'][key]['avail'])
          output = material_consume * product_effic

          model['sectors'][key]['food'] += output
          if (product_effic > 0):
            model['sectors'][key]['avail'] -= math.floor(material_consume/product_effic)
      

  def produce_manufactured_goods(self, model):
    for key in model["sectors"]:
      if model['sectors'][key]['effic'] > 60:
        # lcm production
        # lcm's are in a 1:! ratio with iron
        if model['sectors'][key]['des'] == 17:
          product_effic = model['sectors'][key]['effic'] / 100
          product_effic *= (model['sectors'][key]['iron'] / 100)
          worker_limit = (model['sectors'][key]['avail'] * product_effic) 
          material_limit = model["sectors"][key]["iron"]
          material_consume = min(worker_limit, material_limit)
          output = material_consume * product_effic

          model['sectors'][key]['iron'] -= output
          model['sectors'][key]['lcm'] += output
          if ( product_effic > 0 ):
            model['sectors'][key]['avail'] -= math.floor(material_consume/product_effic)

        # hcm production
        # hcm is 2 iron for 1 hcm
        elif model['sectors'][key]['des'] == 18:
          product_effic = model['sectors'][key]['effic'] / 100
          product_effic *= (model['sectors'][key]['iron'] / 100)
          worker_limit = (model['sectors'][key]['avail'] * product_effic) 
          material_limit = math.floor(model["sectors"][key]["iron"] / 2)
          material_consume = min(worker_limit, material_limit)
          output = material_consume * product_effic

          model['sectors'][key]['iron'] -= output
          model['sectors'][key]['hcm'] += output
          if ( product_effic > 0 ):
            model['sectors'][key]['avail'] -= math.floor(material_consume/product_effic)


  def set_ship_effic(self, model):
    pass

  def food_consumption(self, model):
    for key in model["sectors"]:
      civil = model["sectors"][key]["civil"]
      food_consumed = math.floor(civil * 0.035 )
      sect_food = model["sectors"][key]["food"]
      food_remaining = sect_food - food_consumed
      if food_remaining < 0:
        food_remaining = 0
      model["sectors"][key]["food"] = food_remaining


  def population_growth(self, model):
    growth_rate = 2
    for key in model["sectors"]:
      civils = model["sectors"][key]["civil"]
      food = model["sectors"][key]["food"]
      food_needed = math.floor( civils * 0.035 )
      if food >= food_needed:
        civils += civils * growth_rate
        if civils > 1000:
          civils = 1000
        model["sectors"][key]["civil"] = civils
      else:
        food_diff = food_needed - food
        unfed_civils = math.floor(food_diff / 0.035)
        new_civils = civils - unfed_civils
        if new_civils < 0:
          new_civils = 0
        model["sectors"][key]["civil"] = new_civils

  def refil_mobility(self, model):
    for key in model['sectors']:
      if model["sectors"][key]["mobil"] < 127:
        model["sectors"][key]["mobil"] += 60
        if model["sectors"][key]["mobil"] > 127:
          model["sectors"][key]["mobil"] = 127


      
  def run(self, model):
    #prepare stage
    self.set_avail(model)
    self.refil_mobility(model)
    self.food_consumption(model)

    #production stage
    self.set_effic(model)
    self.set_ship_effic(model)
    self.harvest_natural_resources(model)
    self.produce_manufactured_goods(model)
    self.population_growth(model)
    self.send_to_distribution(model)
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
