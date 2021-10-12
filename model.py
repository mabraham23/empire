import sys
import os
import pickle
import copy

from actions import Move

def createModel():
  if os.path.exists("data/country.p"):
    fin = open("data/country.p", "rb")
    country = pickle.load(fin)
    fin.close()
  else:
    print("country file not created")

  if os.path.exists("data/sectors.p"):
    fin = open("data/sectors.p", "rb")
    sectors = pickle.load(fin)
    fin.close()
  else:
    print("sectors file not created")
  
  if os.path.exists("data/ship.p"):
    fin = open("data/ship.p", "rb")
    ships = pickle.load(fin)
    fin.close()
  else:
    print("ships file not created")

  model = {}
  sectors_copy = copy.deepcopy(sectors)
  country_copy = copy.deepcopy(country)
  ships_copy = copy.deepcopy(ships)
  model["country"] = country_copy
  model["sectors"] = sectors_copy
  model["ships"] = ships_copy
  return model

def show(self):
  for key in self.model:
    print()
    print(key)
  for skey in self.model["sectors"]:
    print()
    print(skey)
    print(self.model["sectors"][skey])
    print()
    print()

def getkey(self, key):
  print(self.model[key])

# def run():
#   m = createModel()
#   M = Move('civil', '(-1, -3)', 100, '(0, 0)')
#   M.move(m)
#   # print(type(model))
#   # print(model["country"])
#   # move.move(model)

# run()
  
