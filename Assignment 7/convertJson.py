import sys
import json

#nodes = 32
obj = { "nodes" : [], "links" : [] }
count = 0

f = open("matrix.dat")
g = f.readlines()
f.close()

#grab and process the weights
for line in g[34]:
    name = count + 1
    Node = {'id' : str(name)}
    obj['nodes'].append(Node)
    col = line.split()
    for j in range(len(col)):
        if col[j] != "0":
            source = count
            weight = int(col[j])
            target = j
            newLink = \
                { "source" :source, "target" :target, "weight" :weight }
            obj['links'].append(newLink)
    count = count + 1
print(json.dumps(obj))
    