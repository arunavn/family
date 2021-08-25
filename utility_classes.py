class Member:
    """
    Member class defines the structure to 
    hold all relevant information about a 
    family member, incluiding his/her level
    in the tree, level 0 being the root 
    """
    def __init__(self, name, gender = 'F', mother = None, father = None, partner = None, level = 0):
        self.name = name
        self.gender = gender
        self.partner = partner
        self.mother = mother
        self.father = father
        self.level = level
    def update_member(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class FamilyTree:
    """
    The FamilyTree class defines the 
    tree(in list variable "__tree") and 
    various methods to perform 
    operation on tree,it has a variable
     '__levels' which holds number 
     of members in each level.
    member at same level are stored
    toghether in the list for fast traversal
    """
    def __init__(self):
        self.__tree = [] 
        self.__levels = []


    def get_new_mebmer_template(self, name, gender = 'F', mother_name = None, partner_name= None):
        member, mother, father, partner, level = Member(name= name, gender= gender), None, None, None, 0
        if mother_name is not None:
            mother = self.get_member_by_name(mother_name)
            if isinstance(mother, Member):
                if mother.gender != 'F':
                    return 'CHILD_ADDITION_FAILED'
                father = mother.partner
                level = mother.level + 1            
        elif partner_name is not None:
             partner = self.get_member_by_name(partner_name)
             if isinstance(partner, Member):
                level = partner.level
        if mother is None and partner is None and len(self.__tree) !=0:
            return 'PERSON_NOT_FOUND'
        member.update_member(father=father, mother= mother, partner= partner, level= level)
        if partner is not None:
                partner.update_member(partner = member)
        return member
    

    def add_member_to_tree(self, member):
        if not isinstance(member, Member):
            return 'CHILD_ADDITION_FAILED'
        tree_len = len(self.__tree)
        try:
            ins_pos = sum( [ i for i in self.__levels[:member.level+1] ])     
        except IndexError:
            ins_pos  = tree_len
        self.__tree.insert(ins_pos, member)
        return member


    def update_levels(self, inserted_at):
        level = inserted_at
        if len(self.__levels) - 1 >=  level:
            self.__levels[level] = self.__levels[level] + 1
            return
        level_tmp = [0 for j in range(0, level - len(self.__levels) )]
        if len(level_tmp) > 0:
            level_tmp[-1] = 1
        else:
            level_tmp = [1]
        self.__levels+= level_tmp


    def add_member(self, name, gender = 'F', mother_name = None, partner_name= None):
        member = self.get_new_mebmer_template(name, gender = gender, mother_name = mother_name, partner_name= partner_name)
        if not isinstance(member, Member):
            print(member)
            return member
        self.add_member_to_tree(member)
        if not isinstance(member, Member):
            return member
        self.update_levels(inserted_at= member.level)


    def get_member_by_name(self, name):
        for member in self.__tree:
            if member.name == name:
                return member


    def get_tree(self):
        tree = []
        for member in self.__tree:
            node = member.__dict__
            for key, val in node.items():
                if isinstance(val, Member):
                    node[key] = val.name
            tree.append(node)
        return tree 


    def create_initial_tree(self, initial_tree):
        for m in initial_tree:
            self.add_member(name = m['name'], gender = m['gender'], mother_name = m['mother'], partner_name= m['partner'])


    def get_members_at_level(self, level):
        if level >= len(self.__levels): return []
        start = sum( [ i for i in self.__levels[:level] ])
        stop = start + self.__levels[level]
        members = self.__tree[start:stop]
        return members


    def get_siblings(self, member, male = True, female = True):
        if isinstance(member, str): member = self.get_member_by_name(member)
        if member is None:  return [ None, 'PERSON_NOT_FOUND']
        siblings = []
        if not isinstance( member.mother, Member):
            return [None, 'NONE'] 
        filt = lambda x: ( isinstance(x.mother, Member) and 
                        member.mother.name == x.mother.name
                        and x.name != member.name )
        potential_siblings = list( filter( filt, self.get_members_at_level(member.level) ) )
        for ps in potential_siblings:
            if male and (ps.gender == 'M'):
                siblings.append(ps)
            if female and (ps.gender == 'F'):
                siblings.append(ps)
        if len(siblings) == 0: return [None, 'NONE'] 
        return siblings


    def get_offsprings(self, member, male = True, female = True):
        if isinstance(member, str): member = self.get_member_by_name(member)
        if member is None:  return [ None, 'PERSON_NOT_FOUND']
        filt = lambda x: member in [ x.mother, x.father]
        potential_offsprings = self.get_members_at_level(member.level + 1)
        offsprings_all, offsprings = list(filter(filt, potential_offsprings)), []
        for oa in offsprings_all:
            if male and (oa.gender == 'M'):
                offsprings.append(oa)
            if female and (oa.gender == 'F'):
                offsprings.append(oa)
        if len(offsprings) == 0: return [None, 'NONE']       
        return offsprings

    def get_parents_siblings(self, member, side, male= True, female= True):
        if isinstance(member, str): member = self.get_member_by_name(member)
        if member is None:  return [ None, 'PERSON_NOT_FOUND']
        parent = self.get_parents(member)[side]
        parent_siblings = self.get_siblings(parent, male= male, female = female)
        member_list =  parent_siblings
        if len(member_list) == 0: return [None, 'NONE']
        return member_list
    
    def get_parents(self, member):
        parents = {"mother": None, "father": None}
        potential_parents = self.get_members_at_level(member.level - 1)
        for pp in potential_parents:
            if pp == member.father:
                parents['father'] = pp
            if pp == member.mother:
                parents['mother'] = pp               
        return parents


    def get_in_laws(self, member, male = True, female = True):
        if isinstance(member, str): member = self.get_member_by_name(member)
        if member is None:  return [ None, 'PERSON_NOT_FOUND']
        spouse_siblings = []
        if member.partner is not None:
            spouse_siblings = self.get_siblings(member.partner, male = male, female = female)
            spouse_siblings = [] if spouse_siblings[0] == None else spouse_siblings
        sibling_partners = []
        siblings = self.get_siblings(member, male = male, female = female)
        siblings = [] if siblings[0] == None else siblings
        for s in siblings:
            if s.partner is not None:
                sibling_partners.append(s.partner)
        member_list = spouse_siblings + sibling_partners
        if len(member_list) == 0: return [None, 'NONE']
        return member_list


class InputHandler:
    def __init__(self, ftree):
        self.__ftree = ftree

    def add_child(self, mother_name, name, gender):
        msg = self.__ftree.add_member(name, gender[0], mother_name)
        if isinstance(msg, str):
            return msg
        else:
            return 'CHILD_ADDITION_SUCCEEDED'

            
    def get_relationship(self, member_name, relation):
        member_list = [None, 'NONE']
        if relation in ['Paternal-Uncle', 'Paternal-Aunt', 'Maternal-Uncle', 'Maternal-Aunt']:
            side = 'father' if relation.split('-')[0] == 'Paternal' else 'mother'
            male = True if relation.split('-')[1] == 'Uncle' else False
            member_list = self.__ftree.get_parents_siblings(member_name, side, male= male, female= not(male))
        elif relation in ['Son', 'Daughter']:
            male = True if relation == 'Son' else False
            member_list  = self.__ftree.get_offsprings(member_name, male = male, female = not(male))
        elif relation in ['Siblings']:
            member_list = self.__ftree.get_siblings(member_name, male = True, female = True)
        elif relation in ['Sister-In-Law', 'Brother-In-Law']:
            male = True if relation.split('-')[0] == 'Brother' else False
            member_list = self.__ftree.get_in_laws(member_name, male = male, female = not(male))
        output = '' 
        if member_list[0] is None:
            output = member_list[1]
        else:
            mname_list = [m.name for m in member_list]
            output = ' '.join(mname_list)
        return output


    def handle_input(self, lines):
        output = []
        for l in lines:
            words = l.strip().split()
            desired_method = words[0].strip()
            if desired_method == 'ADD_CHILD':
                if len(words) == 4:
                    mother_name, name, gender = words[1], words[2], words[3]
                    msg = self.add_child(mother_name, name, gender)
                    output.append(msg)
                else:
                    output.append('CHILD_ADDITION_FAILED')
            elif desired_method == 'GET_RELATIONSHIP':

                if len(words) == 3:
                    m_string = self.get_relationship(words[1], words[2])
                    output.append(m_string)
                else:
                    output.append("NONE")
        return output