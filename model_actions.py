from actions import Action


class Model_Actions():

  def __init__(self, actions_list):
    self.actions_list = actions_list

  def macro_designate(self, state):
    # two strategies for designating sectors
    pass

  def macro_populate(self, state):
    # two strategies for distributing food and people
    pass

  def macro_distribute(self, state):
    # one strategy for setting distribution center and thresholds
    pass

  def build(self, state):
    #decide when it's time to build 
    pass

  def create_actions(self, state):
    # list of possible actions to take based on state
    pass

def result(state_1, actions_list):
  # create state_2 based on running actions_list with new state
  model_copy = copy.deepcopy(state_1.model)
  for action in actions_list:
    action.run(model_copy)

  state_2 = state(model_copy, parent, arriving_action, path_cost)

def goal(state):
  # check if goal has been reached
  pass

def step_cost(state_1, a, state_2):
  # update = cost of 1.0
  # else 0.01 * number of prmitive commands in action
  pass 

    
