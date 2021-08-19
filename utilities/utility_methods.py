def add_child(ftree, mother_name, name, gender):
    name, mother_name, gender = name.lower(), mother_name.lower(), gender[0]
    msg = ftree.add_member(name, gender, mother_name)
    if isinstance(msg, str):
        return msg
    else:
        return 'CHILD_ADDITION_SUCCEEDED'
        

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
    return output
