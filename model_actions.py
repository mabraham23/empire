from abc import abstractproperty
from actions import Action, Build, Capital, Designate, Distribute, Threshold, Move
from model import createModel
from state import State
from update_simulator import Update, print_country
import copy
import math


class Model_Actions():

  def __init__(self):
    pass


  def sort_model_by(self, model, item, remaining):
    new_sort_dict = {}
    for key in model:
      if key in remaining:
        item_amount = model[key][item]
        new_sort_dict[key] = item_amount
      else:
        continue
    return new_sort_dict

  def print_actions(self, actions):
    print(actions)

  def macro_designate(self, state):

    # if a designation strategy has been made, don't change it
    strategy_made = False
    for key in state.model['sectors']:
      if state.model["sectors"][key]["des"] == 24:
        strategy_made = True

    if not strategy_made:
      return [[]]


    moves_list = []
    mineral_heavy_list = []
    fert_heavy_list = []

    mineral_dict = {}
    fert_dict = {}
    min_sector_list = []
    fert_sector_list = []
    for key in state.model['sectors']:
      # populate sector list
      min_sector_list.append(key)
      fert_sector_list.append(key)
      # populate mineral dict
      sect_mineral = state.model['sectors'][key]['min']
      mineral_dict[key] = sect_mineral
      # populate fert dict
      sect_fert = state.model['sectors'][key]['fert']
      fert_dict[key] = sect_fert


    # mining heavy designate
    # keep 0,0 as the capital
    min_sector_list.remove('(0, 0)')
    for i in range(4):
      model_item_dict = self.sort_model_by(state.model['sectors'], 'min', min_sector_list)
      max_key = max(model_item_dict, key=model_item_dict.get)
      min_sector_list.remove(max_key)
      if state.model["sectors"][max_key]["des"] != 10:
        d = Designate(max_key, "m")
        mineral_heavy_list.append(d)
    for i in range(2):
      model_item_dict = self.sort_model_by(state.model['sectors'], 'fert', min_sector_list)
      max_key = max(model_item_dict, key=model_item_dict.get)
      min_sector_list.remove(max_key)
      if state.model["sectors"][max_key]["des"] != 15:
        d = Designate(max_key, "a")
        mineral_heavy_list.append(d)
    # set harbor
    for sect in min_sector_list:
      if state.model['sectors'][sect]['coastal'] == 1:
        min_sector_list.remove(sect)
        if state.model["sectors"][sect]["des"] != 12:
          d = Designate(sect, "h")
          mineral_heavy_list.append(d)
        break
    if state.model["sectors"][min_sector_list[0]]["des"] != 17:
      a = Designate(min_sector_list[0], "j")
      mineral_heavy_list.append(a)
    if state.model["sectors"][min_sector_list[1]]["des"] != 18:
      b = Designate(min_sector_list[1], "k")
      mineral_heavy_list.append(b)

    fert_sector_list.remove('(0, 0)')
    for i in range(4):
      model_item_dict = self.sort_model_by(state.model['sectors'], 'fert', fert_sector_list)
      max_key = max(model_item_dict, key=model_item_dict.get)
      fert_sector_list.remove(max_key)
      if state.model["sectors"][max_key]["des"] != 15:
        d = Designate(max_key, "a")
        fert_heavy_list.append(d)
    for i in range(2):
      model_item_dict = self.sort_model_by(state.model['sectors'], 'iron', fert_sector_list)
      max_key = max(model_item_dict, key=model_item_dict.get)
      fert_sector_list.remove(max_key)
      if state.model["sectors"][max_key]["des"] != 10:
        d = Designate(max_key, "m")
        fert_heavy_list.append(d)
    # set harbor
    for sect in fert_sector_list:
      if state.model['sectors'][sect]['coastal'] == 1:
        fert_sector_list.remove(sect)
        if state.model["sectors"][sect]["des"] != 12:
          d = Designate(sect, "h")
          fert_heavy_list.append(d)
        break
    if state.model["sectors"][fert_sector_list[0]]["des"] != 17:
      a = Designate(fert_sector_list[0], "j")
      fert_heavy_list.append(a)
    if state.model["sectors"][fert_sector_list[1]]["des"] != 18:
      b = Designate(fert_sector_list[1], "k")
      fert_heavy_list.append(b)

    moves_list.append(fert_heavy_list)
    moves_list.append(mineral_heavy_list)
    return moves_list


  def macro_populate(self, state):
    moves_list = []
    pop_dict = {}
    mine_pop = 0
    agr_pop = 0
    city_pop = 0
    lcm_pop = 0
    hcm_pop = 0
    harb_pop = 0
    total_iron = 0
    total_food = 0
    total_pop = 0
    num_sects = 0
    for key in state.model['sectors']:
      pop_dict[key] = state.model["sectors"][key]["civil"]
      total_pop += state.model["sectors"][key]["civil"]
      total_iron+= state.model["sectors"][key]["iron"]
      total_food+= state.model["sectors"][key]["food"]
      num_sects += 1
      # mine
      if state.model['sectors'][key]['des'] == 10:
        mine_pop += state.model["sectors"][key]["civil"]
      # agribusiness
      elif state.model['sectors'][key]['des'] == 15:
        agr_pop += state.model["sectors"][key]["civil"]

      # capital or city population
      elif state.model['sectors'][key]['des'] == 5:
        city_pop += state.model["sectors"][key]["civil"]

      # harbor population
      elif state.model['sectors'][key]['des'] == 12:
        harb_pop += state.model["sectors"][key]["civil"]

      # lcm population
      elif state.model['sectors'][key]['des'] == 17:
        lcm_pop += state.model["sectors"][key]["civil"]

      # hcm population
      elif state.model['sectors'][key]['des'] == 18:
        hcm_pop += state.model["sectors"][key]["civil"]

    # agriculture heavy 
    # 3 agric 40 %
    # 3 mine  20 %   
    # 1 lcm   10 % 
    # 1 hcm   10 %
    # 1 city  10 %
    # 1 harbor 10 %

    # evenly distribute
    even_pop = math.floor( total_pop / num_sects)
    over = []
    under = []
    small_list = []
    for key in state.model['sectors']:
      if state.model['sectors'][key]['civil'] > even_pop:
        over_item = {}
        over_item["sect"] = key
        over_item["civil"] = state.model['sectors'][key]['civil']
        over_item["mobil"] = state.model['sectors'][key]['mobil']
        over.append(over_item)
        
      else:
        small_list.append(key)
        under_item = {}
        under_item["sect"] = key
        under_item["civil"] = state.model['sectors'][key]['civil']
        under.append(under_item)

      
    for big in over:
      m = Move()
      move_amounts = m.calc_max_move_list(state.model, big["sect"], small_list, "civil", even_pop)
      for sect in move_amounts:
        m = Move("civil", big["sect"], sect["amount"], sect["dest"])
        moves_list.append(m)

    return [moves_list]



  def macro_distribute(self, state):
    actions_list = []
    # find distribution center
    dist_center = ""
    for key in state.model['sectors']:
      if state.model['sectors'][key]["newdes"] in [12, 13]:
        dist_center = key
    for key in state.model['sectors']:
      pop = state.model['sectors'][key]['civil']
      if pop > 0:
        opt_thresh = round(pop / 2.5)
        f_dist = state.model['sectors'][key]['f_dist']
        if f_dist != opt_thresh:
          t = Threshold('food', key, opt_thresh)
          actions_list.append(t)
      # lcm and hcm
      if state.model['sectors'][key]['newdes'] == 17 or state.model['sectors'][key]['newdes'] == 18:
        if state.model['sectors'][key]['i_dist'] < 500: 
          t = Threshold('iron', key, 500)
          actions_list.append(t)
        if state.model['sectors'][key]['newdes'] == 17:
          if state.model['sectors'][key]['l_dist'] != 1: 
            t = Threshold('lcm', key, 1)
            actions_list.append(t)
        if state.model['sectors'][key]['newdes'] == 18:
          if state.model['sectors'][key]['h_dist'] != 1: 
            t = Threshold('hcm', key, 1)
            actions_list.append(t)

      #mines
      if state.model['sectors'][key]['newdes'] == 10:
        if state.model['sectors'][key]['i_dist'] != 1:
          t = Threshold('iron', key, 1)
          actions_list.append(t)



      a = Action()
      x = state.model['sectors'][key]['xdist']
      y = state.model['sectors'][key]['ydist']
      coord = a.intsToCoord(x, y)
      if coord != dist_center:
        d = Distribute(key, dist_center)
        actions_list.append(d)

    return [actions_list]


  def macro_update(self, state):
    actions_list =[]
    u = Update()
    actions_list.append(u)
    return [actions_list]

  def build(self, state):
    moves_list = []
    if len(state.model['ships']) < 1:
      harb = ""
      for key in state.model["sectors"]:
        if state.model["sectors"][key]["des"] == 12:
          harb = key
      if harb != "": 
        b = Build("ship", harb, "fishing", 1)
        moves_list.append(b)
    return [moves_list]

  # returns a list of actions
  def create_actions(self, state):
    arriving = state.arriving_action
    if (state.arriving_action == "update" or state.arriving_action == "start"):
      return self.macro_designate(state), "designate"
    elif (state.arriving_action == "designate"):
      return self.macro_populate(state), "populate"
    elif (state.arriving_action == "populate"):
      return self.macro_distribute(state), "distribute"
    elif (state.arriving_action == "distribute"):
      return self.build(state), "build"
    elif (state.arriving_action == "build"):
      return self.macro_update(state), "update"
    else:
      print("invalid state action")
      
  def result(self, state_1, actions_list, arriving_action):
    model_copy = copy.deepcopy(state_1.model)
    primitives = []
    if len(actions_list) > 0:
      for action in actions_list:
        if arriving_action != "update":
          p = action.run(model_copy)
          if p != None:
            primitives.append(p)
        else:
          p = action.run(model_copy)
          primitives.append("UPDATE")
    else:
      primitives = []
    
    state_2 = State(model_copy, state_1, primitives, arriving_action, self.step_cost(arriving_action, len(actions_list)))
    return state_2

  def goal(self, state):
    max_pop = True
    for key in state.model["sectors"]:
      if state.model["sectors"][key]["civil"] < 1000:
        max_pop = False
        break
    if len(state.model["ships"]) >= 1 and max_pop:
      return True
    return False

  def step_cost(self, arriving_action, primitive_commands):
    if arriving_action == "update":
      return 1
    else:
      return 0.01 * primitive_commands

    
