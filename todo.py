import argparse
import os
import re

TODODIR = u"D:\\My Dropbox\\todo"
# 0 = quiet
# 1 = verbose
# 2 = debug
TODOVERBOSE = 2


def get_linecount(filename):
    count = 0
    with open(filename, "r") as f:
        for line in f:
            count += 1
    padding = 0
    if count < 10:
        padding = 1
    elif count < 100:
        padding = 2
    elif count < 1000:
        padding = 3
    elif count < 10000:
        padding = 4
    return count, padding


def add(args):
    filename = os.path.join(TODODIR, "todo.txt")

    if TODOVERBOSE:
        print "Opening {0}".format(filename)

    with open(filename, "a+") as f:
        f.write(args.task)


def append(args):
    todotxt = os.path.join(TODODIR, "todo.txt")
    lines = []
    with open(todotxt) as f:
        lineno = 0
        for line in f:
            lineno += 1
            lines.append(line.strip())
            if lineno == args.task:
                lines[lineno - 1] += " " + args.text
    with open(todotxt, "w") as f:
        for line in lines:
            f.write(line)
            f.write("\n")




def archive(args):
    todotxt = os.path.join(TODODIR, "todo.txt")
    donetxt = os.path.join(TODODIR, "done.txt")
    todolines = []
    donelines = []
    with open(todotxt) as f:
        for line in f:
            if line[0:2] == "x ":
                donelines.append(line)
            else:
                todolines.append(line)
    with open(todotxt, "w") as f:
        for line in todolines:
            f.write(line)
    with open(donetxt, "a") as f:
        for line in donelines:
            f.write(line)


def delete(args):
    todotxt = os.path.join(TODODIR, "todo.txt")
    lines = []
    with open(todotxt) as f:
        for line in f:
            lines.append(line)
    if len(args.term) == 0:
        lines[args.task - 1 : args.task] = []
    else:
        print "DELETE TERM NOT YET IMPLEMENTED"
    with open(todotxt, "w") as f:
        for line in lines:
            f.write(line)


def depri(args):
    print "DEPRIORITIZE NOT YET IMPLEMENTED"


def do_tasks(args):
    filename = os.path.join(TODODIR, "todo.txt")

    if TODOVERBOSE == 2:
        print "Opening {0}".format(filename)

    lines = []
    with open(filename) as f:
        for l in f:
            lines.append(l)

    for t in args.task:
        if t <= 0:
            sys.exit()

    lineno = 0

    for line in lines:
        lineno += 1
        if lineno in args.task:
            if lines[lineno - 1][0:2] == "x ":
                print "Task is already marked done!"
            else:
                print "Marked '{0}' as done.".format(lines[lineno - 1].strip())
                lines[lineno - 1] = "x " + lines[lineno - 1]

    with open(filename, 'w') as f:
        for line in lines:
            f.write(line)


def list_tasks(args):
    filename = os.path.join(TODODIR, "todo.txt")

    if TODOVERBOSE == 2:
        print "Opening {0}".format(filename)

    totallines, padding = get_linecount(filename)
    with open(filename) as f:
        current_line = 0
        for line in f:
            match = True
            for term in args.term:
                if term[0] == "-" and line.find(term[1:]) == -1:
                    match = match or True
                elif line.find(term) != -1:
                    match = match or True
                else:
                    match = False
            current_line += 1
            if match:
                print "{1:{0}d} ".format(padding, current_line) + line.strip()



def listall(args):
    print "LISTALL NOT YET IMPLEMENTED"


def list_contexts(args):
    filename = os.path.join(TODODIR, "todo.txt")

    if TODOVERBOSE == 2:
        print "Opening {0}".format(filename)

    with open(filename) as f:
        seen = []
        for line in f:
            for mdata in re.findall("@(\w+)", line):
                if mdata not in seen:
                    seen.append(mdata)
                    print "@{0}".format(mdata)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser("add", help="add help")
    parser_add.add_argument("task", help="task help")
    parser_add.set_defaults(func=add)

    parser_append = subparsers.add_parser("append", help="append help")
    parser_append.add_argument("task", type=int, help="task help")
    parser_append.add_argument("text", help="text help")
    parser_append.set_defaults(func=append)

    parser_archive = subparsers.add_parser("archive", help="archive help")
    parser_archive.set_defaults(func=archive)

    parser_del = subparsers.add_parser("delete", help="delete help")
    parser_del.add_argument("task", type=int, help="task help")
    parser_del.add_argument("term", nargs="*", help="term help")
    parser_del.set_defaults(func=delete)

    parser_depri = subparsers.add_parser("depri", help="deprioritize help")
    parser_depri.add_argument("task", type=int, nargs="+", help="task help")
    parser_depri.set_defaults(func=depri)

    parser_do = subparsers.add_parser("do", help="do help")
    parser_do.add_argument("task", type=int, nargs="+", help="task help")
    parser_do.set_defaults(func=do_tasks)

    parser_list = subparsers.add_parser("list", help="list help")
    parser_list.add_argument("term", nargs="*", help="term help")
    parser_list.set_defaults(func=list_tasks)

    parser_listall = subparsers.add_parser("listall", help="listall help")
    parser_listall.add_argument("term", nargs="*", help="term help")
    parser_listall.set_defaults(func=listall)

    parser_listcon = subparsers.add_parser("listcon", help="list contexts help")
    parser_listcon.set_defaults(func=list_contexts)

    args = parser.parse_args()
    args.func(args)


parse_args()
