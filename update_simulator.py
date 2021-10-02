import sys
import os
import pickle
import copy

sys.path.append(".")

from actions import Action, Move, Distribute, Threshold, Designate, Build, Capital
from model import *

class Update():

  def __init__(self):
    self.sectors = {}
    self.country = {}
    self.dist_items = ['c_dist','m_dist','s_dist','g_dist','p_dist','i_dist','d_dist','b_dist','f_dist','o_dist','l_dist','h_dist','u_dist','r_dist']
    self.dist_dict = {'c_dist': 'civil','m_dist': 'milit','s_dist': 'shell','g_dist':'gun','p_dist':'petrol','i_dist':'iron','d_dist':'dust','b_dist': 'bar','f_dist':'food','o_dist':'oil','l_dist':'lcm','h_dist':'hcm','u_dist': 'uw','r_dist': 'rad'}

  def getUpdatedSectors(self):
    if os.path.exists("sectors.p"):
      fin = open("sectors.p", "rb")
      bad_sectors = pickle.load(fin)
      fin.close()

      sectors = {}
      for key in bad_sectors:
        new = copy.deepcopy(bad_sectors[key])
        sectors[key] = new
      self.sectors = sectors
    
    if os.path.exists("country.p"):
      fin = open("country.p", "rb")
      self.country = pickle.load(fin)
      fin.close()

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

  def show(self):
    self.getUpdatedSectors()
    print()
    print(self.country)
    print()
    for key in self.sectors:
      print()
      print(key, ":")
      print(self.sectors[key])
      print()

  def show_sect(self, x, y):
    self.getUpdatedSectors()
    sect = "(" + str(x) + ", " + str(y) + ")"
    print()
    print(sect)
    print()
    for key in self.sectors[sect]:
      print(key, ":", self.sectors[sect][key])
    print()
  
  def save(self):
    fout = open("sectors.p", "wb")
    pickle.dump(self.sectors, fout)
    fout.close()

    fout = open("country.p", "wb")
    pickle.dump(self.country, fout)
    fout.close()
  
  def calculateAvail(self, civ, sctwork, milit, uw):
    etu = 60
    avail = round((civ * sctwork / 100.0 + milit / 2.5 + uw) * etu / 100.0)
    return avail
      
  def update(self):
    self.getUpdatedSectors()

    print()
    # print("before", self.sectors['(0, 0)'])
    print()
    for key in self.sectors:
      # calculate and set avail for each sector
      self.sectors[key]['avail'] = self.calculateAvail(self.sectors[key]['civil'], self.sectors[key]['work'], self.sectors[key]['milit'], self.sectors[key]['uw'])
      # send materials from sectors to distribution center
      # for item in self.dist_items:
      des = self.sectors[key]['des']
      if ( des != "h" or des != "c"):
        item = self.getItemFromDes(key)
        thresh = self.sectors[key][item]
        if thresh > 0:
          amount = self.sectors[key][self.dist_dict[item]]
          if amount > thresh:
            num = amount - thresh
          dest = "(" + str(self.sectors[key]['xdist']) + ", " + str(self.sectors[key]['ydist']) + ")"
          move_item = self.dist_dict[item]
          m = Move(move_item, key, num, dest)
          m.dist_move()

    print()
    print("after", self.sectors['(0, 0)'])
    print()
        


      # if ( self.sectors[key]['newdes'] != self.sectors[key]['des'] ):
      #   self.sectors[key]['des'] = self.sectors[key]['newdes']
      


def runCommands():
  model = createModel()
  M = Move('civil', '(-1, -3)', 100, '(0, 0)')
  M.move(model) 
  # Model = Model()
  # model.move()
  # model.capital()

  # model.run()
  # model = Model()

  # move = Move('civil', '(-1, -3)', 100, '(0, 0)')
  # model.exec(move)
  # update = update()
  # model.exec(update)
  # a = Action()
  # u = Update()
  # u.show()
  # u.show()
  # a.save()
  # u.show()
  # u.show()
  # A = Action()
  # A.show_items()
  # m = Move('civil', '(-1, -3)', 100, '(0, 0)')
  # m.move()
  # m.save()
  # m.show_sect('(0, 0)')
  # m.move()
  # m.show_sect('(0, 0)')
  # m.save()
  # u = Update()
  # u.update()
  # u.show_sect(0,0)
  # u.update()
  # u = Update()
  # d = Designate('(0, 2)', 'c')
  # d.designate()
  # d.save()
  # u.update()
  # u.save()
  # d.save()
  # u.update()
  # u.save()
  # C = Capital('(0, 2)')
  # C.capital()
  # C.save()


  # d.show()


runCommands()