from utilities.utility_classes import FamilyTree
import json

#creating initial tree dictionary from input json
intial_tree = {}
with open('data_source/initial_tree.json', 'r') as f: 
    intial_tree = json.load(f)

#creating initial tree with initial tree dictionary
ftree = FamilyTree()
ftree.create_initial_tree(initial_tree=intial_tree)



ini_tree = ftree.get_tree()
# ini_tree = []
# l = ftree.get_members_at_level(3)
# print(l)
# for i in l:
#     ini_tree.append(i.__dict__)
y = json.dumps(ini_tree)
print(y)



