"""
by Denexapp

"""


def read(f):
    try:
        read_file = open(f)
    except:
        read_file = open(f, "w")
        read_file.write("0")
        read_file.close()
    read_file = open(f)
    var = int(read_file.read())
    read_file.close()
    return var


def write(f, value):
    write_file = open(f, "w")
    write_file.write(str(value))
    write_file.close()
