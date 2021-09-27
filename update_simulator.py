import sys
import os
import pickle
import copy

sys.path.append(".")

from actions import Action, Move, Distribute, Threshold, Designate, Build, Capital

class Update():

  def __init__(self):
    self.sectors = {}
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
  
  def save(self):
    fout = open("sectors.p", "wb")
    pickle.dump(self.sectors, fout)
    fout.close()
  
  def calculateAvail(self, civ, sctwork, milit, uw):
    etu = 60
    avail = round((civ * sctwork / 100.0 + milit / 2.5 + uw) * etu / 100.0)
    return avail
      
  def update(self):
    self.getUpdatedSectors()

    print()
    print("before", self.sectors['(0, 0)'])
    print()
    for key in self.sectors:
      # calculate and set avail for each sector
      # self.sectors[key]['avail'] = self.calculateAvail(self.sectors[key]['civil'], self.sectors[key]['work'], self.sectors[key]['milit'], self.sectors[key]['uw'])
      # distribute materials
      for item in self.dist_items:
        thresh = self.sectors[key][item]
        if thresh > 0:
          amount = self.sectors[key][self.dist_dict[item]]
          if amount > thresh:
            dist = amount - thresh
          dest = "(" + str(self.sectors[key]['xdist']) + ", " + str(self.sectors[key]['ydist']) + ")"
          m = Move(item, key, dist, dest)
          m.move()
    print()
    print("after", self.sectors['(0, 0)'])
    print()
        


      # if ( self.sectors[key]['newdes'] != self.sectors[key]['des'] ):
      #   self.sectors[key]['des'] = self.sectors[key]['newdes']
      


def runCommands():
  u = Update()
  # d = Designate('(-1, -3)', 'm')
  # d.designate()
  # d.save()
  u.update()
  # u.save()


runCommands()