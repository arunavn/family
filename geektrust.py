from utility_classes import FamilyTree, InputHandler
import json, sys

def main():
    #creating initial tree dictionary from input json
    intial_tree = {}
    try:
        with open('initial_tree.json', 'r') as f: 
            intial_tree = json.load(f)
    except:
        pass
    #creating initial tree with initial tree dictionary
    ftree = FamilyTree()
    ftree.create_initial_tree(initial_tree=intial_tree)
    input_handler = InputHandler(ftree)
    try:
        #taking all input parameters one by one apart from first(python file)
        for file_path in sys.argv[1:]:
            lines = []
            try:
                with open(file_path, 'r') as f:
                    #for each file reading lines
                    lines = f.readlines()
                #for each file, sending all the lines to handler method
                output = input_handler.handle_input(lines)
                for o in output:
                    print(o) 
            except:
                pass      
    except IndexError:
        pass

if __name__ == "__main__":
    main()