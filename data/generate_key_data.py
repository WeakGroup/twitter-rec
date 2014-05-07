import pickle

celebrity = {}
followers = {}
added_total = 0

for i in range(80):
  fname = "checkpt_80_%s" % i
  print fname

  with open(fname) as f:
    data = pickle.load(f)

    for k in data:
      added_followers = 0
      celebrity[k] = data[k] 

      for u in data[k]:
        added_followers += 1
        added_total +=1
        followers[u] = 1

      print "add %s followers" % added_followers


print "Finish"
print "Total celebrities : ", len(celebrity)
print "Total followers : ", len(followers)
print "added total : ", added_total

fl = [f for f in followers]
cl = [c for c in celebrity]

fname = "key_data"

with open(fname, "w") as f:
  print "Begin dump"
  pickle.dump((fl, cl, celebrity), f, protocol=-1)
