def add_child(ftree, mother_name, name, gender):
    # name, mother_name, gender = name.lower(), mother_name.lower(), gender[0]
    msg = ftree.add_member(name, gender[0], mother_name)
    if isinstance(msg, str):
        return msg
    else:
        return 'CHILD_ADDITION_SUCCEEDED'
        

def get_relationship(ftree, member_name, relation):
    member_list = ftree.get_member_by_relation(member_name, relation)
    output = '' 
    if member_list[0] is None:
        output = member_list[1]
    else:
        mname_list = [m.name for m in member_list]
        output = ' '.join(mname_list)
    return output


def handle_input(lines, ftree):
    output = []
    for l in lines:
        words = l.strip().split()
        desired_method = words[0].strip()
        if desired_method == 'ADD_CHILD':
            if len(words) == 4:
                mother_name, name, gender = words[1], words[2], words[3]
                msg = add_child(ftree, mother_name, name, gender)
                output.append(msg)
            else:
                output.append('CHILD_ADDITION_FAILED')
        elif desired_method == 'GET_RELATIONSHIP':
            if len(words) == 3:
                m_string = get_relationship(ftree, words[1], words[2])
                output.append(m_string)
            else:
                output.append("NONE")
    return output
