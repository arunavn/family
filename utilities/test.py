import json
intial_tree = {}
try:
    with open('data_source/initial_tree1.json', 'r') as f: 
        intial_tree = json.load(f)
except:
    pass
for m in intial_tree:
    for key, val in m.items():
        if val is not None:
            val = val.title()
            m[key] = val
with open('data_source/initial_tree.json', 'w') as f1:
    json.dump(intial_tree, f1, indent=True)
print(intial_tree)