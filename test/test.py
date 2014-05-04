import pickle

with open("checkpt.txt") as f:
  data = pickle.load(f)
  print data
