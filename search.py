from model_actions import Model_Actions
from model import createModel
from state import State
from actions import Action

def search(initial_state):
  Q = []
  Q.append(initial_state)
  while len(Q) != 0:
    s = Q.pop()
    m = Model_Actions()
    if m.goal(s):
      return s
    actions, arriving_action = m.create_actions(s)
    if arriving_action == "update":
      print("stop here")
    for a in actions:
      new_state = m.result(s, a, arriving_action)
      for p in new_state.primitives:
        print(p)
      Q.append(new_state)
  return


def find_goal_state():
  initial_model = createModel()
  initial_state = State(initial_model, None, [], "start", 0)
  g = search(initial_state)
  while g.parent_state != None:
    for a in g.primitives:
      print(a)
    g = g.parent_state

find_goal_state()