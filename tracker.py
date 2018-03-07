import uuid

clients_data = {}
groups_members = {}
groups = []

def register(ip, port, username):
    generated_id = uuid.uuid4()
    id = str(generated_id)
    clients_data[id] = (ip, port, username)
    return id

def list_groups():
    return groups

def list_members(group_name):
    members_ids = groups_members[group_name]
    members_names = []
    for member_id in members_ids:
        _, _, name = clients_data[member_id]
        members_names.append(name)
    return members_names

def join_groups(group_name, id):
    # if the group doesn't exist create it & add user to group
    if (not groups_members.has_key(group_name)):
        groups_members[group_name] = []
        groups.append(group_name)

    # now the group exists, (even if it's a null group)
    # so add the user to the group
    groups_members[group_name].append(id)

    # and then return the full list of members
    members_data = []
    for client_id in groups_members[group_name]:
        members_data.append((client_id, ) + clients_data[client_id])
    return  members_data

def exit_group(group_name, id):
    if (not groups_members.has_key(group_name)):
        return False

    # try to delete the user from a pre-specified group
    try:
        groups_members[group_name].remove(id)
    except ValueError:
        print "EXIT_GROUP: User, not member of requested group"
        return False

    # if the group is empty delete it andn remove the corresponding group
    if (groups_members[group_name] == []):
        del groups_members[group_name]
        try:
            groups.remove(group_name)
        except ValueError:
            print "EXIT_GROUP: Group, not found"
            return False

    # Client to exit the group found, everything ok
    print "EXIT_GROUP-FOUND"
    return True


def quit(id):
    # removing user from all groups
    for group_name in groups:
        exit_group(group_name, id)

    print "QUIT_COMPLETED"
    return True






def proccess_message(message):
    if (message.startswith('!')):
        command = message.split(' ')
        cmd = command[0].lstrip('!')
        args_size = len(command) - 1
        print "FULL COMMAND: " + str(command)
        print "ARGS SIZE: " + str(args_size)
        print "CMD: " + cmd

        ## check for errors in arguments
        if (cmd == "r" and args_size != 3):
            return "Invalid arguments", []

        ## the arguments list incldue one extra argument, client id.
        elif (cmd == "lg" and args_size != 1):
            return "Invalid arguments", []
        elif (cmd == "lm" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "j" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "e" and args_size != 2):
            return "Invalid arguments", []
        elif (cmd == "q " and args_size != 1):
            return "Invalid arguments", []

        ## return command with correct arguments
        return cmd, command[1:]
