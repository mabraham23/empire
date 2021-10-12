class State():

  def __init__(self, model, parent_state, primitives, arriving_action, path_cost):
    self.model = model
    self.parent_state = parent_state
    self.primitives = primitives 
    self.arriving_action = arriving_action
    self.path_cost = path_cost
