class Member:
    
    def __init__(self, name, gender = 'F', mother = None, father = None, partner = None, level = 0):
        #Member.member_id+=1 
        self.name = name
        self.gender = gender
        self.partner = partner
        self.mother = mother
        self.father = father
        self.level = level


class FamilyTree:

    def __init__(self):
        self.__tree = [] 
        self.__levels = []


    def add_member(self, name, gender = 'F', mother_name = None, partner_name= None):
        mother = None
        if mother_name is not None:     
            mother = self.get_member_by_name(mother_name)
        if mother is None:
            father = None
        else:
            if mother.gender != 'F':
                return 'CHILD_ADDITION_FAILED'
            father = self.get_member_by_relation(mother, 'partner')[0]
        mname, fname = None, None
        if mother is not None:
            mname = mother.name
        if father is not None:
            fname = father.name
        ins_pos, tree_len = 0, len(self.__tree)
        check_level = -1
        if mother is not None:
            check_level = mother.level
        else:
            partner = self.get_member_by_name(partner_name)
            if partner is not None:
                check_level = partner.level - 1
        if mother is None and partner_name is None:
            return 'PERSON_NOT_FOUND'
        member = Member(name, gender, mname, fname, partner_name, check_level + 1 )
        level = check_level + 1
        try:
            ins_pos = sum( [ i for i in self.__levels[:level+1] ])     
        except IndexError:
            ins_pos  = tree_len

        self.__tree.insert(ins_pos, member)
        if len(self.__levels) - 1 >=  level:
            self.__levels[level] = self.__levels[level] + 1
        else:
            level_tmp = [0 for j in range(0, level - len(self.__levels) )]
            if len(level_tmp) > 0:
                level_tmp[-1] = 1
            else:
                level_tmp = [1]
            for i in level_tmp:
                self.__levels.append(i)
        return member


    def get_member_by_name(self, name):
        for member in self.__tree:
            if member.name == name:
                return member


    def get_member_by_relation(self, member, relation):
        if isinstance(member, str):
            member = self.get_member_by_name(member)
        if member is None:
            return [None]
        member_list= []
        if relation == 'partner':
            member_at_same_level = self.get_members_at_level(member.level)
            for m in member_at_same_level:
                if m.partner is not None:
                    if m.partner == member.name:
                        member_list.append(m)
        elif relation == 'Paternal-Uncle':
            father = self.get_parents(member)['father']
            father_male_siblings = self.get_siblings(father, female = False)
            member_list =  father_male_siblings
        elif relation == 'Paternal-Aunt':
            father = self.get_parents(member)['father']
            father_female_siblings = self.get_siblings(father, male = False)
            member_list =  father_female_siblings
        elif relation == 'Maternal-Uncle':
            mother = self.get_parents(member)['mother']
            mother_male_siblings = self.get_siblings(mother, female = False)
            member_list = mother_male_siblings
        elif relation == 'Maternal-Aunt':
            mother = self.get_parents(member)['mother']
            mother_female_siblings = self.get_siblings(mother, male = False)
            member_list =  mother_female_siblings
        elif relation == 'Son':
            member_list = self.get_offsprings(member, female = False)
        elif relation == 'Daughter':
            member_list = self.get_offsprings(member, male = False)
        elif relation == 'Siblings':
            member_list = self.get_siblings(member)
        if len(member_list) == 0:    
            return [None]
        return member_list
            

    def get_tree(self):
        tree = []
        for member in self.__tree:
            tree.append(member.__dict__)
        print(self.__levels)
        return tree 


    def create_initial_tree(self, initial_tree):
        for m in initial_tree:
            self.add_member(name = m['name'], gender = m['gender'], mother_name = m['mother'], partner_name= m['partner'])


    def get_members_at_level(self, level):
        start = sum( [ i for i in self.__levels[:level] ])
        stop = start + self.__levels[level]
        members = self.__tree[start:stop]
        return members
    
    def get_siblings(self, member, male = True, female = True):
        potential_siblings = self.get_members_at_level(member.level)
        siblings = []
        for ps in potential_siblings:
            if ps.name != member.name and member.mother == ps.mother and member.mother is not None:
                if male and (ps.gender == 'M'):
                    siblings.append(ps)
                if female and (ps.gender == 'F'):
                    siblings.append(ps)
        return siblings

    def get_offsprings(self, member, male = True, female = True):
        potential_offsprings = self.get_members_at_level(member.level + 1)
        offsprings = []
        for po in potential_offsprings:
            if (  member.name in [ po.mother, po.father]):
                if male and (po.gender == 'M'):
                    offsprings.append(po)
                if female and (po.gender == 'F'):
                    offsprings.append(po)
        return offsprings

    
    def get_parents(self, member):
        parents = {"mother": None, "father": None}
        potential_parents = self.get_members_at_level(member.level - 1)
        for pp in potential_parents:
            if pp.name == member.father:
                parents['father'] = pp
            if pp.name == member.mother:
                parents['mother'] = pp               
        return parents