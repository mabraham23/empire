from actions import Action, Capital, Designate, Distribute, Threshold
from model import createModel
from state import State
from update_simulator import Update
import copy

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

  def macro_designate(self, state):
    moves_list = []
    search_strategy = ""
    mineral_dict = {}
    fert_dict = {}
    sector_list = []
    for key in state.model['sectors']:
      # populate sector list
      sector_list.append(key)
      # populate mineral dict
      sect_mineral = state.model['sectors'][key]['min']
      mineral_dict[key] = sect_mineral
      # populate fert dict
      sect_fert = state.model['sectors'][key]['fert']
      fert_dict[key] = sect_fert
    
    # determine which side is heavy
    min_heavy = 0
    fert_heavy = 0
    for mineral in mineral_dict.values():
      if mineral >  50:
        min_heavy += 1
    for fert in fert_dict.values():
      if fert >  50:
        fert_heavy += 1
    if min_heavy > fert_heavy:
      search_strategy = "mineral"
    elif fert_heavy > min_heavy:
      search_strategy = "fertility"
    else:
      search_strategy = "mineral"

    # execute mineral designate 
    print("designate strategy: ", search_strategy)
    if search_strategy == "mineral":
      # 10 total sectors
      # need 1 harbor, 1 capital, 1 lcm , 1 hcm rest mine or agric
      # 4 mines # 2 agric
      for i in range(3):
        model_item_dict = self.sort_model_by(state.model['sectors'], 'min', sector_list)
        max_key = max(model_item_dict, key=model_item_dict.get)
        sector_list.remove(max_key)
        d = Designate(max_key, "m")
        moves_list.append(d)
      for i in range(1):
        model_item_dict = self.sort_model_by(state.model['sectors'], 'fert', sector_list)
        max_key = max(model_item_dict, key=model_item_dict.get)
        sector_list.remove(max_key)
        d = Designate(max_key, "a")
        moves_list.append(d)
      # set harbor
      for sect in sector_list:
        if state.model['sectors'][sect]['coastal'] == 1:
          sector_list.remove(sect)
          d = Designate(sect, "h")
          moves_list.append(d)
          break
      a = Designate(sector_list[0], "j")
      moves_list.append(a)
      b = Designate(sector_list[1], "k")
      moves_list.append(b)
      c = Designate(sector_list[2], "c")
      # d = Capital(sector_list[2])
      moves_list.append(c)
      # moves_list.append(d)
      return moves_list
      
    elif search_strategy == "fertility":
      for i in range(3):
        model_item_dict = self.sort_model_by(state.model['sectors'], 'fert', sector_list)
        max_key = max(model_item_dict, key=model_item_dict.get)
        sector_list.pop(max_key)
        d = Designate(max_key, "a")
        moves_list.append(d)
      for i in range(1):
        model_item_dict = self.sort_model_by(state.model['sectors'], 'iron', sector_list)
        max_key = max(model_item_dict, key=model_item_dict.get)
        sector_list.pop(max_key)
        d = Designate(max_key, "m")
        moves_list.append(d)
      # set harbor
      for sect in sector_list:
        if state.model['sectors'][sect]['costal'] == 1:
          sector_list.pop(sect)
          d = Designate(sect, "h")
          moves_list.append(d)
          break
      a = Designate(sector_list[0], "j")
      moves_list.append(a)
      b = Designate(sector_list[1], "k")
      moves_list.append(b)
      c = Designate(sector_list[2], "c")
      # d = Capital(sector_list[2])
      moves_list.append(c)
      # moves_list.append(d)
      return moves_list

    else:
      print("invalid designate strategy given")


  def macro_populate(self, state):
    moves_list = []
    stragey = ""
    pop_dict = {}
    mine_pop = 0
    agr_pop = 0
    total_pop = 0
    total_iron = 0
    total_food = 0
    for key in state.model['sectors']:
      pop_dict[key] = state.model["sectors"][key]["civil"]
      total_pop += state.model["sectors"][key]["civil"]
      total_iron+= state.model["sectors"][key]["iron"]
      total_food+= state.model["sectors"][key]["food"]
      # mine
      if state.model['sectors'][key]['des'] == 10:
        mine_pop += state.model["sectors"][key]["civil"]
      # agribusiness
      elif state.model['sectors'][key]['des'] == 15:
        agr_pop += state.model["sectors"][key]["civil"]


  def macro_distribute(self, state):
    actions_list = []
    # find distribution center
    dist_center = ""
    for key in state.model['sectors']:
      if state.model['sectors'][key]["des"] in [12, 13]:
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
      if state.model['sectors'][key]['des'] == 17 or state.model['sectors'][key]['des'] == 18:
        if state.model['sectors'][key]['i_dist'] < 500: 
          t = Threshold('iron', key, 500)
          actions_list.append(t)
      else:
        # no sector should have a threshold for iron except lcm and hcm
        t = Threshold('iron', key, 0)
        actions_list.append(t)

      # set distribution center as harbor
      a = Action()
      x = state.model['sectors'][key]['xdist']
      y = state.model['sectors'][key]['ydist']
      coord = a.intsToCoord(x, y)
      if coord != dist_center:
        d = Distribute(key, dist_center)
        actions_list.append(d)

    return actions_list


  def macro_update(self, state):
    u = Update()
    u.update(state.model)

  def build(self, state):
    #decide when it's time to build 
    pass

  def create_actions(self, state):
    # moves_list = self.macro_designate(state)
    moves_list = self.macro_distribute(state)
    self.result(state, moves_list)
    # if (state.arriving_action == "update"):
    #   self.macro_designate(state)
    # elif (state.arriving_action == "designate"):
    #   self.macro_populate(state)
    # elif (state.arriving_action == "populate"):
    #   self.macro_distribute(state)
    # elif (state.arriving_action == "distribute"):
    #   self.build(state)
    # elif (state.arriving_action == "build"):
    #   self.macro_update(state)
    # else:
    #   print("invalid state action")

      

  def result(self, state_1, actions_list):
    # create state_2 based on running actions_list with new state
    model_copy = copy.deepcopy(state_1.model)
    for action in actions_list:
      action.run(model_copy)
    u = Update()
    print("this is the start ")
    u.show(model_copy)
    

    # state_2 = state(model_copy, parent, arriving_action, path_cost)

  def goal(state):
    # check if goal has been reached
    pass

  def step_cost(state_1, a, state_2):
    # update = cost of 1.0
    # else 0.01 * number of prmitive commands in action
    pass 

def run():
  m = Model_Actions()
  model = createModel()
  d = Designate('(1, -1)', 'm')
  d.run(model)
  d = Designate('(-1, -3)', 'h')
  d.run(model)
  u = Update()
  u.update(model)
  s = State(model, 0, "update", 0)
  m.create_actions(s)

run()
    
