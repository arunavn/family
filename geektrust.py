from utilities.utility_classes import FamilyTree
from utilities.utility_methods import handle_input
import json, sys

def main():
    #creating initial tree dictionary from input json
    intial_tree = {}
    try:
        with open('data_source/initial_tree.json', 'r') as f: 
            intial_tree = json.load(f)
    except:
        pass
    #creating initial tree with initial tree dictionary
    ftree = FamilyTree()
    ftree.create_initial_tree(initial_tree=intial_tree)
    # mem= ftree.get_member_by_name("kriya")
    # x = ftree.get_member_by_relation(mem, 'Siblings')
    # for m in x:
    #     print(m.name)


    try:
        #taking all input parameters one by one apart from first(python file)
        for file_path in sys.argv[1:]:
            lines = []
            # try:
            with open(file_path, 'r') as f:
                #for each file reading lines
                lines = f.readlines()
            #for each file, sending all the lines to handler method
            output = handle_input(lines, ftree)
            for o in output:
                print(o)       
            # except:
            #     print('error')
            #     pass
    except IndexError:
        pass
    ini_tree = ftree.get_tree()
    y = json.dumps(ini_tree)
    # print(y)


if __name__ == "__main__":
    main()