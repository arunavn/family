class Member:
    #member_id = 0
    
    def __init__(self, name, gender = 'F', mother = None, father = None, partner = None, level = 0):
        #Member.member_id+=1 
        self.id = Member.member
        self.name = name
        self.gender = gender
        self.partner = partner
        self.mother = mother
        self.father = father
        self.level = level

class FamilyTree:

    def __init__(self):
        self.tree = [] 
        self.levels = []


    def add_member(self, name, gender = 'F', mother_name = None, partner_name= None):
        mother = self.get_member_by_name(mother_name)
        father = self.get_member_by_relation(mother, 'partner')
        partner = self.get_member_by_name(partner_name)
        mother_id, father_id, partner_id, level = None, None, None, 0
        if mother is not None:
            level = int(mother.level) + 1
            mother_id = mother.id
        if father is not None:
            father_id = father.id
        if partner is not None:
            partner_id = partner.id
        member = Member(name, gender, mother_id, father_id, partner_id, level )
        ins_pos, tree_len = 0, len(self.tree)
        for i, v in enumerate(self.tree):
            if v.level > mother.level:
                ins_pos = i
            if i == tree_len - 1:
                ins_pos = tree_len
        self.tree.insert(ins_pos, member)
        if len(self.levels) - 1 >=  level:
            self.levels[level]+= self.levels[level] + 1
        else:
            level_tmp = [0 for j in range(0, level - len(self.levels) )]
            level_tmp[-1] = 1
            self.levels.append(level_tmp)



    def get_member_by_name(self, name):
        pass


    def get_member_by_id(self, id):
        pass

    def get_member_by_relation(self, member, relation):
        pass

