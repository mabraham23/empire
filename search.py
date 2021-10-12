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
    new_state = m.result(s, actions, arriving_action)
    Q.append(new_state)
  return

initial_model = createModel()
initial_state = State(initial_model, 0, "update", 0)
search(initial_state)