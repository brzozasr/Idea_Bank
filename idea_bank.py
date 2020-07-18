import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
file = "idea_bank.txt"
data_file = os.path.join(current_dir, file)
list_of_ideas = []


def is_positive_int(str):
    try:
        num = int(str)
        if num < 0:
            return False
    except ValueError:
        return False
    return True


def load_data_from_file():
    # Checking that file exist if not create it.
    if not os.path.exists(data_file):
        fo = open(data_file, "w")
        fo.close()

    # Load data to the list
    with open(data_file, "r") as ideas_file:
        for idea in ideas_file:
            idea = idea.strip(os.linesep)
            list_of_ideas.append(idea)


def argv():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--add":
            return sys.argv[1:]
        elif sys.argv[1] == "--delete":
            return sys.argv[1:]
        else:
            return sys.argv[1]
    else:
        return None


def help_idea_bank():
    print("""--run:      running the program in the command line (terminal mod).
--help:     shows available commands.
--list:     lists all saved ideas.
--add:      adding a new idea to the lists.
            REQUIRED ARGUMENT: text a  new idea e.g. "--add The super new idea."
--delete:   removes the idea from the list by index.
            REQUIRED ARGUMENT: index of the idea e.g. "--delete 2"
--exit:     the program termination.""")


def error_info():
    print('\x1b[0;37;41m', "There is no such command!", '\x1b[0m')


def list_ideas():
    if len(list_of_ideas) > 0:
        i = 1
        for idea in list_of_ideas:
            print(f"{i}. {idea}")
            i += 1
    else:
        print("There are no ideas on the list.")


def add_idea(idea):
    if type(idea) == list:
        if len(idea) > 0:
            join_idea = " ".join(idea)
            list_of_ideas.append(join_idea)

            with open(data_file, "a") as ideas_file:
                ideas_file.write(join_idea)
                ideas_file.write("\n")

            list_ideas()
    else:
        print('\x1b[0;37;41m', "Specify an idea after --add!", '\x1b[0m')


def del_idea(id):
    idea = list_of_ideas.pop(id - 1)

    # Write data to the list
    with open(data_file, "w+") as ideas_file:
        for idea in list_of_ideas:
            ideas_file.write(idea)
            ideas_file.write("\n")

    print(f"The idea \"{idea}\" was deleted!")


def command_chooser(command):
    if command == "--help":
        help_idea_bank()
    elif command.startswith("--add"):
        idea = command.split(" ")
        if len(idea) > 1 and idea[1] != "":
            add_idea(idea[1:])
        else:
            print('\x1b[0;37;41m', "Specify an idea after --add!", '\x1b[0m')
    elif command.startswith("--delete"):
        del_id = command.split(" ")
        list_len = len(list_of_ideas)
        if list_len > 0:
            if len(del_id) > 1 and del_id[1] != "" and is_positive_int(del_id[1]):
                id = int(del_id[1]) - 1
                if list_len > id >= 0:
                    del_idea(int(del_id[1]))
                else:
                    print('\x1b[0;37;41m', f"The integer must be in range 1 to {list_len}!", '\x1b[0m')
            else:
                print('\x1b[0;37;41m', f"Specify an integer after --delete in range 1 to {list_len}!", '\x1b[0m')
        else:
            print('\x1b[0;37;41m', "There are no ideas to delete!", '\x1b[0m')
    elif command == "--list":
        list_ideas()
    else:
        error_info()


def main():
    while True:
        command = input("idea_bank :\\> ")

        if command == "--exit":
            break
        else:
            command_chooser(command)


# Load data from the file and put into list line by line
load_data_from_file()

if argv() == "--run":
    print("What is your new idea? To add to the list use the command: \"--add Your idea.\".")
    print("For help write a command \"--help\" or \"--exit\" to terminate.")
    main()
elif argv() == "--help":
    help_idea_bank()
elif type(argv()) == list and argv()[0] == "--add":
    if len(argv()) > 1 and argv()[1] != "":
        add_idea(sys.argv[2:])
    else:
        print('\x1b[0;37;41m', "Specify an idea after --add!", '\x1b[0m')
elif type(argv()) == list and argv()[0] == "--delete":
    list_len = len(list_of_ideas)
    if list_len > 0:
        if len(argv()) > 1 and is_positive_int(argv()[1]) and (list_len > (int(argv()[1]) - 1) >= 0):
            del_idea(int(sys.argv[2]))
        else:
            print('\x1b[0;37;41m', f"Specify an integer after --delete in range 1 to {list_len}!", '\x1b[0m')
    else:
        print('\x1b[0;37;41m', "There are no ideas to delete!", '\x1b[0m')
elif argv() == "--list":
    list_ideas()
else:
    print('\x1b[0;30;42m', "An argument is missing, e.g. \"--run\"!", '\x1b[0m')
    print('\x1b[0;30;42m', "For more info at the end of command write  \"--help\"!", '\x1b[0m')
