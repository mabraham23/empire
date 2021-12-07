from model_actions import Model_Actions
from model import createModel
from state import State

def search(initial_state):
  Q = []
  Q.append(initial_state)
  while len(Q) != 0:
    s = Q.pop()
    m = Model_Actions()
    if m.goal(s):
      return s
    actions, arriving_action = m.create_actions(s)
    for a in actions:
      new_state = m.result(s, a, arriving_action)
      Q.append(new_state)
  return


def find_goal_state():
  initial_model = createModel()
  initial_state = State(initial_model, None, [], "start", 0)
  g = search(initial_state)
  instructions = []
  print()
  print()
  print("COMMANDS START HERE:")
  print()
  print()
  while g.parent_state != None:
    for a in g.primitives[::-1]:
      instructions.insert(0, a)
      # print(a)
    g = g.parent_state
  
  for instr in instructions:
    if instr == "UPDATE":
      break
    else:
      print(instr)


find_goal_state()